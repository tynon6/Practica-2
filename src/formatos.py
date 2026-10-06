"""Importación y exportación inversas para JFLAP .jff, JSON y XML."""
from __future__ import annotations

import json
from pathlib import Path
import xml.etree.ElementTree as ET

from automata import Automaton, normalize_symbol


def _from_records(data: dict) -> Automaton:
    states = data.get("estados", data.get("states", []))
    states = [s.get("nombre", s.get("name")) if isinstance(s, dict) else str(s) for s in states]
    initial = data.get("inicial", data.get("initial", data.get("initial_state", "")))
    if isinstance(initial, dict):
        initial = initial.get("nombre", initial.get("name", ""))
    accepting = data.get("aceptacion", data.get("accepting", data.get("accepting_states", [])))
    accepting = [s.get("nombre", s.get("name")) if isinstance(s, dict) else str(s) for s in accepting]
    alphabet = data.get("alfabeto", data.get("alphabet", []))
    transitions: dict[tuple[str, str], set[str]] = {}
    for transition in data.get("transiciones", data.get("transitions", [])):
        source = transition.get("desde", transition.get("source", transition.get("from")))
        symbol = normalize_symbol(transition.get("lee", transition.get("symbol", transition.get("read", ""))))
        targets = transition.get("hacia", transition.get("destinations", transition.get("to", [])))
        if isinstance(targets, str):
            targets = [targets]
        transitions.setdefault((str(source), symbol), set()).update(map(str, targets))
    return Automaton(states, alphabet, str(initial), set(accepting), transitions)


def _to_records(machine: Automaton) -> dict:
    return {
        "tipo": "AFND-lambda" if machine.has_lambda else "AFND" if machine.nondeterministic else "AFD",
        "alfabeto": machine.alphabet,
        "estados": machine.states,
        "inicial": machine.initial,
        "aceptacion": [s for s in machine.states if s in machine.accepting],
        "transiciones": [
            {"desde": source, "lee": symbol, "hacia": sorted(targets)}
            for (source, symbol), targets in sorted(machine.transitions.items())
        ],
    }


def from_jff(root: ET.Element) -> Automaton:
    automaton = root.find("automaton")
    if automaton is None:
        raise ValueError("El archivo .jff no contiene un elemento <automaton>.")
    states: list[str] = []
    id_to_name: dict[str, str] = {}
    initial = None
    accepting: set[str] = set()
    for state in automaton.findall("state"):
        state_id = state.get("id", "")
        name = state.get("name", state_id)
        states.append(name)
        id_to_name[state_id] = name
        if state.find("initial") is not None:
            initial = name
        if state.find("final") is not None:
            accepting.add(name)
    transitions: dict[tuple[str, str], set[str]] = {}
    alphabet: list[str] = []
    for transition in automaton.findall("transition"):
        source_id = transition.findtext("from", "")
        target_id = transition.findtext("to", "")
        symbol = normalize_symbol(transition.findtext("read", ""))
        if source_id not in id_to_name or target_id not in id_to_name:
            raise ValueError("Una transición .jff apunta a un identificador de estado inexistente.")
        if symbol and symbol not in alphabet:
            alphabet.append(symbol)
        transitions.setdefault((id_to_name[source_id], symbol), set()).add(id_to_name[target_id])
    if initial is None:
        raise ValueError("El archivo .jff no define un estado inicial.")
    return Automaton(states, alphabet, initial, accepting, transitions)


def dumps(machine: Automaton, file_format: str) -> str:
    file_format = file_format.lower().lstrip(".")
    if file_format == "json":
        return json.dumps(_to_records(machine), ensure_ascii=False, indent=2) + "\n"
    if file_format == "xml":
        root = ET.Element("automata", {"tipo": _to_records(machine)["tipo"]})
        alphabet = ET.SubElement(root, "alfabeto")
        for symbol in machine.alphabet:
            ET.SubElement(alphabet, "simbolo").text = symbol
        states = ET.SubElement(root, "estados")
        for name in machine.states:
            attrs = {"nombre": name}
            if name == machine.initial:
                attrs["inicial"] = "true"
            if name in machine.accepting:
                attrs["aceptacion"] = "true"
            ET.SubElement(states, "estado", attrs)
        transitions = ET.SubElement(root, "transiciones")
        for (source, symbol), targets in sorted(machine.transitions.items()):
            for target in sorted(targets):
                ET.SubElement(transitions, "transicion", {"desde": source, "lee": symbol, "hacia": target})
        return ET.tostring(root, encoding="unicode", xml_declaration=True) + "\n"
    if file_format == "jff":
        root = ET.Element("structure")
        ET.SubElement(root, "type").text = "fa"
        body = ET.SubElement(root, "automaton")
        ids = {name: str(i) for i, name in enumerate(machine.states)}
        for i, name in enumerate(machine.states):
            state = ET.SubElement(body, "state", {"id": ids[name], "name": name})
            ET.SubElement(state, "x").text = str(100 + (i % 4) * 150)
            ET.SubElement(state, "y").text = str(100 + (i // 4) * 130)
            if name == machine.initial:
                ET.SubElement(state, "initial")
            if name in machine.accepting:
                ET.SubElement(state, "final")
        for (source, symbol), targets in sorted(machine.transitions.items()):
            for target in sorted(targets):
                edge = ET.SubElement(body, "transition")
                ET.SubElement(edge, "from").text = ids[source]
                ET.SubElement(edge, "to").text = ids[target]
                ET.SubElement(edge, "read").text = symbol
        return ET.tostring(root, encoding="unicode", xml_declaration=True) + "\n"
    raise ValueError(f"Formato no compatible: {file_format!r}. Use jff, json o xml.")


def loads(content: str, file_format: str) -> Automaton:
    file_format = file_format.lower().lstrip(".")
    if file_format == "json":
        return _from_records(json.loads(content))
    if file_format in {"xml", "jff"}:
        root = ET.fromstring(content)
        if root.tag == "structure":
            return from_jff(root)
        if root.tag != "automata":
            raise ValueError("El documento XML no tiene una raíz <automata> ni es un .jff válido.")
        alphabet = [node.text or "" for node in root.findall("./alfabeto/simbolo")]
        states: list[str] = []
        initial = None
        accepting: set[str] = set()
        for node in root.findall("./estados/estado"):
            name = node.get("nombre", "")
            states.append(name)
            if node.get("inicial", "false").lower() == "true":
                initial = name
            if node.get("aceptacion", "false").lower() == "true":
                accepting.add(name)
        transitions: dict[tuple[str, str], set[str]] = {}
        for node in root.findall("./transiciones/transicion"):
            key = (node.get("desde", ""), normalize_symbol(node.get("lee", "")))
            transitions.setdefault(key, set()).add(node.get("hacia", ""))
        if initial is None:
            raise ValueError("El XML no define un estado inicial.")
        return Automaton(states, alphabet, initial, accepting, transitions)
    raise ValueError(f"Formato no compatible: {file_format!r}. Use jff, json o xml.")


def load_automaton(path: str | Path) -> Automaton:
    path = Path(path)
    return loads(path.read_text(encoding="utf-8"), path.suffix)


def save_automaton(machine: Automaton, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dumps(machine, path.suffix), encoding="utf-8")
