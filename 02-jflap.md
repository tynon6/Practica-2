# Ejercicio 2. AFND y AFND-λ en JFLAP

## 2.1. Clasificación y cobertura

### Cobertura de las Listas
Se ha completado e implementado el 100% de la cobertura para la **Lista 2 (ejercicios 94 a 150)** y la **Lista 3 (ejercicios 151 a 263)**. Los archivos `.jff`, `.json` y `.xml` de cada autómata están organizados dentro del directorio `automatas/` en sus respectivas subcarpetas:
- `automatas/lista2-afd/`
- `automatas/lista3-afnd/`
- `automatas/lista3-afnd-lambda/`

---

### Tabla de Clasificación y Justificación

| Ejercicios | Tipo de Autómata | Ubicación en Repositorio | Justificación de Clasificación |
| :--- | :--- | :--- | :--- |
| **94 a 115** | **AFD** (Determinista) | `automatas/lista2-afd/` | Cada estado posee exactamente una transición definida para cada símbolo del alfabeto Σ = {0, 1}, sin ninguna ambigüedad. |
| **116 a 150** | **AFND** (No Determinista Estándar) | `automatas/lista3-afnd/` | Presenta múltiples bifurcaciones o caminos paralelos ante un mismo símbolo de entrada, sin hacer uso de transiciones nulas (λ). |
| **151 a 263** | **AFND-λ** (Con transiciones lambda) | `automatas/lista3-afnd-lambda/` | Utiliza transiciones vacías (λ) para estructurar de manera modular los bloques de uniones, concatenaciones y cierres de Kleene de la expresión regular. |

---
