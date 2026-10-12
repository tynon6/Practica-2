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

## 2.2. Diseño y validación

A continuación se documenta el proceso de diseño, la justificación de la solución y las pruebas de validación para un autómata representativo de la **Lista 3** (`Ejercicio 238`).

### Caso de Estudio: Ejercicio 238
- **Expresión Regular:** `(01 | 10)* (00 | 11) (01 | 10)*`
- **Ubicación del archivo:** `automatas/lista3-afnd-lambda/ejercicio_238.jff`

#### 1. Justificación del Diseño
El autómata se construyó modularmente mediante el algoritmo de Thompson:
1. **Bloque Inicial `(01 | 10)*`:** El estado inicial `q0` permite mediante bucles alternos procesar cualquier combinación de parejas `01` o `10`.
2. **Infijo Obligatorio `(00 | 11)`:** Se requiere indispensablemente el consumo del patrón `00` o `11` para transitar desde `q0` hasta el estado `q5`.
3. **Bloque Final `(01 | 10)*`:** Alrededor del estado final `q5`, mediante transiciones $\lambda$, se enlazan bucles para permitir cualquier sufijo compuesto por `01` o `10`.

#### 2. Tabla de Validación de Cadenas (5 Válidas y 5 Inválidas)

Se evaluaron 10 cadenas mediante la herramienta *Multiple Run* de JFLAP:

| Cadena de Entrada | Tipo de Cadena | Resultado Esperado | Resultado JFLAP | Estado |
| :--- | :--- | :--- | :--- | :--- |
| `00` | Válida | Aceptar | Accept | ✅ Pasó |
| `11` | Válida | Aceptar | Accept | ✅ Pasó |
| `0100` | Válida | Aceptar | Accept | ✅ Pasó |
| `1011` | Válida | Aceptar | Accept | ✅ Pasó |
| `011110` | Válida | Aceptar | Accept | ✅ Pasó |
| `0` | Inválida | Rechazar | Reject | ✅ Pasó |
| `1` | Inválida | Rechazar | Reject | ✅ Pasó |
| `01` | Inválida | Rechazar | Reject | ✅ Pasó |
| `10` | Inválida | Rechazar | Reject | ✅ Pasó |
| `0110` | Inválida | Rechazar | Reject | ✅ Pasó |

> **Evidencia en JFLAP:**
> ![Prueba de múltiples cadenas en JFLAP](../evidencias/jflap/ejercicio_238.png)

#### 3. Simulación Paso a Paso y Caminos Múltiples

Con la herramienta *Step with State* para la cadena `0100`:
- **Inicio:** El autómata evalúa la lectura del prefijo `01` retornando a `q0`.
- **Bifurcación:** Ante el siguiente `0`, el autómata bifurca un camino intentando reconocer la pareja `01` y otro hacia el infijo obligatorio `00`.
- **Aceptación:** Solo la rama que procesa la segunda '0' alcanza el estado de éxito `q5`, demostrando la selección correcta de caminos no deterministas.
