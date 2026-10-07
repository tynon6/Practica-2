"""Modelo independiente de Flet para autómatas finitos (AFD, AFND y AFND-λ)."""
from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict, deque
from typing import Iterable

EPSILON = ""


def normalize_symbol(symbol: str | None) -> str:
    symbol = "" if symbol is None else str(symbol).strip()
    return "" if symbol in {"", "λ", "ε", "lambda", "epsilon"} else symbol


@dataclass
class Automaton:
    states: list[str]
    alphabet: list[str]
    initial: str
    accepting: set[str]
    transitions: dict[tuple[str, str], set[str]]

    def __post_init__(self) -> None:
        self.states = list(dict.fromkeys(str(s).strip() for s in self.states if str(s).strip()))
        self.alphabet = list(dict.fromkeys(normalize_symbol(s) for s in self.alphabet))
        if EPSILON in self.alphabet:
            self.alphabet.remove(EPSILON)
        self.accepting = set(self.accepting)
        cleaned: dict[tuple[str, str], set[str]] = defaultdict(set)
        for (source, symbol), destinations in self.transitions.items():
            cleaned[(str(source), normalize_symbol(symbol))].update(map(str, destinations))
        self.transitions = dict(cleaned)
        if not self.states:
            raise ValueError("El autómata debe tener al menos un estado.")
        if self.initial not in self.states:
            raise ValueError(f"El estado inicial {self.initial!r} no está definido.")
        if not self.accepting <= set(self.states):
            raise ValueError("Hay estados de aceptación que no están definidos.")
        for (source, symbol), destinations in self.transitions.items():
            if source not in self.states or not destinations <= set(self.states):
                raise ValueError(f"Transición con estado no definido: {source!r} → {destinations!r}.")
            if symbol != EPSILON and symbol not in self.alphabet:
                raise ValueError(f"El símbolo {symbol!r} no pertenece al alfabeto.")

    @property
    def nondeterministic(self) -> bool:
        return any(len(targets) > 1 for targets in self.transitions.values()) or self.has_lambda

    @property
    def has_lambda(self) -> bool:
        return any(symbol == EPSILON for _, symbol in self.transitions)

    def destinations(self, state: str, symbol: str) -> set[str]:
        return set(self.transitions.get((state, symbol), set()))

    def lambda_closure(self, states: Iterable[str]) -> set[str]:
        return self.lambda_closure_with_moves(states)[0]

    def lambda_closure_with_moves(self, states: Iterable[str]) -> tuple[set[str], list[tuple[str, str, str]]]:
        """Calcula la clausura y conserva las transiciones λ recorridas."""
        closure = set(states)
        # Procesa los estados en un orden estable para que la traza sea reproducible.
        pending = sorted(closure, reverse=True)
        moves: list[tuple[str, str, str]] = []
        while pending:
            state = pending.pop()
            for target in sorted(self.destinations(state, EPSILON)):
                moves.append((state, EPSILON, target))
                if target not in closure:
                    closure.add(target)
                    pending.append(target)
        return closure, moves

    def trace(self, word: str) -> list[dict[str, object]]:
        """Regresa configuraciones después de cada símbolo, incluyendo λ-clausura."""
        if any(len(symbol) != 1 for symbol in self.alphabet):
            raise ValueError("La simulación de la interfaz requiere símbolos de un carácter.")
        if any(char not in self.alphabet for char in word):
            bad = next(char for char in word if char not in self.alphabet)
            raise ValueError(f"El símbolo {bad!r} no pertenece al alfabeto.")
        current, epsilon_moves = self.lambda_closure_with_moves({self.initial})
        trace: list[dict[str, object]] = [{
            "index": 0, "symbol": None, "states": sorted(current), "moves": [],
            "lambda_moves": epsilon_moves,
        }]
        for index, symbol in enumerate(word, start=1):
            moves = [
                (state, symbol, target)
                for state in sorted(current)
                for target in sorted(self.destinations(state, symbol))
            ]
            next_states = {target for _, _, target in moves}
            current, epsilon_moves = self.lambda_closure_with_moves(next_states)
            trace.append({
                "index": index, "symbol": symbol, "states": sorted(current), "moves": moves,
                "lambda_moves": epsilon_moves,
            })
        return trace

    def accepts(self, word: str) -> bool:
        return bool(set(self.trace(word)[-1]["states"]) & self.accepting)

    def transition_table(self) -> list[tuple[str, list[str]]]:
        symbols = list(self.alphabet) + ([EPSILON] if self.has_lambda else [])
        rows = []
        for state in self.states:
            cells = [", ".join(sorted(self.destinations(state, symbol))) or "—" for symbol in symbols]
            rows.append((state, cells))
        return rows


def from_definition(alphabet: str, states: str, initial: str, accepting: str, transitions: str) -> Automaton:
    """Lee la definición editable: una transición por línea, `q0, a -> q1, q2`."""
    state_names = [part.strip() for part in states.split(",") if part.strip()]
    symbols = [part.strip() for part in alphabet.split(",") if part.strip()]
    accepting_names = {part.strip() for part in accepting.split(",") if part.strip()}
    mapping: dict[tuple[str, str], set[str]] = defaultdict(set)
    for number, line in enumerate(transitions.splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "->" not in line:
            raise ValueError(f"Línea {number}: se esperaba `origen, símbolo -> destino(s)`. ")
        left, right = line.split("->", 1)
        fields = [item.strip() for item in left.split(",", 1)]
        if len(fields) != 2 or not fields[0] or not fields[1]:
            raise ValueError(f"Línea {number}: indique el estado de origen y el símbolo leído.")
        symbol = normalize_symbol(fields[1])
        for target in (part.strip() for part in right.split(",")):
            if target:
                mapping[(fields[0], symbol)].add(target)
    return Automaton(state_names, symbols, initial.strip(), accepting_names, dict(mapping))
