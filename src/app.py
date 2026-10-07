import flet as ft
from flet import app, AppView
from lenguajes import prefijos, sufijos, subcadenas, kleene_y_positiva

def main(page: ft.Page):
    page.title = "Operaciones Básicas sobre Lenguajes"
    page.scroll = ft.ScrollMode.AUTO

    # Operación 1
    input_cadena = ft.TextField(label="Cadena de entrada (e.g. abc)", width=300)
    res_op1 = ft.Text(selectable=True)

    def procesar_op1(e):
        w = input_cadena.value or ""
        p = prefijos(w)
        s = sufijos(w)
        sub = subcadenas(w)
        res_op1.value = (
            f"Prefijos ({len(p)}): {p}\n"
            f"Sufijos ({len(s)}): {s}\n"
            f"Subcadenas ({len(sub)}): {sub}"
        )
        page.update()

    # Operación 2
    input_alfabeto = ft.TextField(label="Alfabeto (e.g. a,b)", width=300)
    input_longitud = ft.TextField(label="Longitud máxima", width=150)
    res_op2 = ft.Text(selectable=True)

    def procesar_op2(e):
        try:
            raw_alf = input_alfabeto.value or ""
            alf = [s.strip() for s in raw_alf.split(",") if s.strip()]
            n = int(input_longitud.value or "0")
            
            estrella, mas = kleene_y_positiva(alf, n)
            res_op2.value = (
                f"Σ* ({len(estrella)} cadenas):\n{estrella}\n\n"
                f"Σ+ ({len(mas)} cadenas):\n{mas}"
            )
        except ValueError as err:
            res_op2.value = f"Error: {err}"
        page.update()

    page.add(
        ft.Text("Operación 1: Prefijos, Sufijos y Subcadenas", size=18, weight=ft.FontWeight.BOLD),
        input_cadena,
        ft.ElevatedButton("Calcular", on_click=procesar_op1),
        res_op1,
        ft.Divider(),
        ft.Text("Operación 2: Cerraduras Σ* y Σ+", size=18, weight=ft.FontWeight.BOLD),
        ft.Row([input_alfabeto, input_longitud]),
        ft.ElevatedButton("Generar Cerraduras", on_click=procesar_op2),
        res_op2
    )

if __name__ == "__main__":
    app(target=main, view=AppView.WEB_BROWSER, port=8550, host="0.0.0.0")
