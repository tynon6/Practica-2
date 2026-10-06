"""Interfaz Flet del simulador. El núcleo y los lectores no dependen de Flet."""
from __future__ import annotations

import base64
import json
from pathlib import Path

import flet as ft

from automata import Automaton, from_definition
from formatos import load_automaton, save_automaton
from lenguajes import kleene_y_positiva, prefijos, subcadenas, sufijos
from visualizacion import draw_automaton


def main(page: ft.Page) -> None:
    page.title = "Simulador de autómatas finitos"
    page.window_width = 1180
    page.window_height = 900
    page.scroll = ft.ScrollMode.AUTO

    alphabet = ft.TextField(label="Alfabeto (separa símbolos con coma)", value="a, b", width=520)
    states = ft.TextField(label="Estados", value="q0, q1", width=520)
    initial = ft.TextField(label="Estado inicial", value="q0", width=250)
    accepting = ft.TextField(label="Estados de aceptación", value="q1", width=250)
    transitions = ft.TextField(
        label="Transiciones: origen, símbolo -> destino(s); usa λ o ε para una transición vacía",
        value="q0, a -> q1\nq0, b -> q0\nq1, a -> q1\nq1, b -> q0",
        multiline=True, min_lines=4, max_lines=8, width=800,
    )
    path_field = ft.TextField(label="Ruta del archivo (.jff, .json, .xml)", width=520)
    word_field = ft.TextField(label="Cadena de entrada", width=260)
    operation_word = ft.TextField(label="Cadena para operaciones de lenguajes", width=320)
    max_length = ft.TextField(label="Longitud máxima", value="3", width=150)
    feedback = ft.Text()
    table = ft.Column(spacing=4)
    editor = ft.Column(spacing=4)
    graph = ft.Image(width=820, height=380, fit=ft.ImageFit.CONTAIN)
    trace_view = ft.Column(spacing=4)
    operation_result = ft.Text(selectable=True)
    current: Automaton | None = None
    trace: list[dict[str, object]] = []
    cursor = 0
    cell_fields: dict[tuple[str, str], ft.TextField] = {}

    def present(machine: Automaton) -> None:
        nonlocal current, trace, cursor
        current = machine
        trace = []
        cursor = 0
        trace_view.controls = []
        alphabet.value = ", ".join(machine.alphabet)
        states.value = ", ".join(machine.states)
        initial.value = machine.initial
        accepting.value = ", ".join(s for s in machine.states if s in machine.accepting)
        transition_lines = []
        for (source, symbol), targets in sorted(machine.transitions.items()):
            transition_lines.append(f"{source}, {symbol or 'λ'} -> {', '.join(sorted(targets))}")
        transitions.value = "\n".join(transition_lines)
        symbols = list(machine.alphabet) + ([""] if machine.has_lambda else [])
        cell_fields.clear()
        editor.controls = [ft.Text("Edición interactiva de transiciones (varios destinos separados por coma)", weight=ft.FontWeight.BOLD)]
        editor.controls.append(ft.Row([ft.Text("Estado", width=110), *[ft.Text(s or "λ", width=130) for s in symbols]]))
        for state in machine.states:
            row = [ft.Text(state, width=110)]
            for symbol in symbols:
                field = ft.TextField(
                    value=", ".join(sorted(machine.destinations(state, symbol))),
                    label=symbol or "λ", width=130, dense=True,
                )
                cell_fields[(state, symbol)] = field
                row.append(field)
            editor.controls.append(ft.Row(row, scroll=ft.ScrollMode.AUTO))
        png = draw_automaton(machine)
        graph.src_base64 = base64.b64encode(png).decode("ascii")
        graph.update()
        headers = ["Estado", *machine.alphabet, *(["λ"] if machine.has_lambda else [])]
        table.controls = [ft.Text("Tabla de transiciones", weight=ft.FontWeight.BOLD)]
        table.controls.append(ft.Text("  |  ".join(headers), font_family="monospace", weight=ft.FontWeight.BOLD))
        for state, cells in machine.transition_table():
            flags = ("→ " if state == machine.initial else "  ") + ("* " if state in machine.accepting else "  ")
            table.controls.append(ft.Text(flags + state + "  |  " + "  |  ".join(cells), font_family="monospace"))
        feedback.value = f"Autómata cargado: {len(machine.states)} estados, {len(machine.alphabet)} símbolos; " + ("no determinista" if machine.nondeterministic else "determinista")
        page.update()

    def build(_=None) -> None:
        try:
            if cell_fields:
                transitions.value = "\n".join(
                    f"{state}, {symbol or 'λ'} -> {field.value}"
                    for (state, symbol), field in cell_fields.items() if (field.value or "").strip()
                )
            present(from_definition(alphabet.value or "", states.value or "", initial.value or "", accepting.value or "", transitions.value or ""))
        except Exception as error:
            feedback.value = f"No se pudo definir el autómata: {error}"
            page.update()

    def _build_from_fields() -> None:
        cell_fields.clear()
        build()

    def import_file(_=None) -> None:
        try:
            present(load_automaton(path_field.value or ""))
            feedback.value = f"Importado desde {path_field.value}"
            page.update()
        except Exception as error:
            feedback.value = f"No se pudo importar: {error}"
            page.update()

    def export_file(_=None) -> None:
        try:
            if current is None:
                build()
            if current is None:
                return
            save_automaton(current, path_field.value or "automata.jff")
            feedback.value = f"Autómata guardado en {path_field.value or 'automata.jff'}"
            page.update()
        except Exception as error:
            feedback.value = f"No se pudo exportar: {error}"
            page.update()

    def start_simulation(_=None) -> None:
        nonlocal trace, cursor
        try:
            if current is None:
                build()
            if current is None:
                return
            trace = current.trace(word_field.value or "")
            cursor = 0
            accepted = bool(set(trace[-1]["states"]) & current.accepting)
            feedback.value = "Cadena aceptada." if accepted else "Cadena rechazada."
            trace_view.controls = [ft.Text(f"{len(trace) - 1} símbolos; resultado: {'aceptada' if accepted else 'rechazada'}", weight=ft.FontWeight.BOLD)]
            page.update()
        except Exception as error:
            feedback.value = f"No se pudo simular: {error}"
            page.update()

    def format_trace_step(index: int) -> ft.Text:
        item = trace[index]
        symbol = "inicio" if item["symbol"] is None else repr(item["symbol"])
        moves = item["moves"] or []
        epsilon_moves = item["lambda_moves"] or []
        move_text = ", ".join(f"{a} --{s}--> {b}" for a, s, b in moves) or "sin transición consumible"
        epsilon_text = ", ".join(f"{a} --λ--> {b}" for a, _, b in epsilon_moves)
        if epsilon_text:
            move_text += f"; λ-clausura: {epsilon_text}"
        return ft.Text(f"Paso {index} ({symbol}): {{{', '.join(item['states'])}}}; {move_text}")

    def step_simulation(_=None) -> None:
        nonlocal cursor
        if not trace:
            start_simulation()
        if not trace:
            return
        trace_view.controls.append(format_trace_step(cursor))
        cursor = min(cursor + 1, len(trace) - 1)
        page.update()

    def show_complete_trace(_=None) -> None:
        nonlocal cursor
        if not trace:
            start_simulation()
        if not trace:
            return
        accepted = bool(set(trace[-1]["states"]) & current.accepting) if current else False
        trace_view.controls = [ft.Text(
            f"Recorrido completo: {'aceptada' if accepted else 'rechazada'}",
            weight=ft.FontWeight.BOLD,
        )]
        trace_view.controls.extend(format_trace_step(index) for index in range(len(trace)))
        cursor = len(trace) - 1
        page.update()

    def reset_simulation(_=None) -> None:
        nonlocal trace, cursor
        trace = []
        cursor = 0
        trace_view.controls = []
        feedback.value = "Traza reiniciada."
        page.update()

    def run_operation(kind: str) -> None:
        value = operation_word.value or ""
        try:
            if kind == "kleene":
                if current is None:
                    build()
                symbols = current.alphabet if current else [x.strip() for x in (alphabet.value or "").split(",") if x.strip()]
                star, positive = kleene_y_positiva(symbols, int(max_length.value or "0"))
                result = {"Σ*": star, "Σ+": positive}
            else:
                result = {"prefijos": prefijos(value), "sufijos": sufijos(value), "subcadenas": subcadenas(value)}[kind]
            operation_result.value = json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as error:
            operation_result.value = f"Error: {error}"
        page.update()

    page.add(
        ft.Text("Simulador de autómatas finitos", size=28, weight=ft.FontWeight.BOLD),
        ft.Text("Defina o importe un AFD, AFND o AFND-λ. Las transiciones λ se escriben como λ, ε o símbolo vacío."),
        ft.Row([alphabet]), ft.Row([states]), ft.Row([initial, accepting]), transitions,
        ft.ElevatedButton("Definir desde los campos", on_click=lambda _: _build_from_fields()),
        ft.Text("Tabla de transición editable"), editor,
        ft.Row([ft.ElevatedButton("Aplicar tabla", on_click=build), path_field,
                ft.ElevatedButton("Importar", on_click=import_file), ft.ElevatedButton("Exportar", on_click=export_file)]),
        feedback,
        ft.Text("Diagrama del autómata", size=20, weight=ft.FontWeight.BOLD), graph, table,
        ft.Divider(), ft.Text("Simulación", size=20, weight=ft.FontWeight.BOLD),
        ft.Row([word_field,
                ft.ElevatedButton("Validar cadena", on_click=start_simulation),
                ft.ElevatedButton("Siguiente paso", on_click=step_simulation),
                ft.ElevatedButton("Mostrar traza completa", on_click=show_complete_trace),
                ft.ElevatedButton("Reiniciar", on_click=reset_simulation)]),
        trace_view,
        ft.Divider(), ft.Text("Operaciones sobre cadenas y lenguajes (Práctica 1)", size=20, weight=ft.FontWeight.BOLD),
        ft.Row([operation_word, ft.ElevatedButton("Prefijos", on_click=lambda _: run_operation("prefijos")),
                ft.ElevatedButton("Sufijos", on_click=lambda _: run_operation("sufijos")),
                ft.ElevatedButton("Subcadenas", on_click=lambda _: run_operation("subcadenas"))]),
        ft.Row([max_length, ft.ElevatedButton("Σ* y Σ+", on_click=lambda _: run_operation("kleene"))]),
        operation_result,
    )
    build()


if __name__ == "__main__":
    ft.app(target=main)
