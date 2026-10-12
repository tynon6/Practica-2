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

## 2.3. Transiciones lambda

### 1. Justificación del Uso y Ubicación de las Transiciones Lambda ($\lambda$)
En el desarrollo de los autómatas de la **Lista 3** (como el Ejercicio 238), las transiciones $\lambda$ desempeñan un rol estructural clave:
- **Modularidad del diseño:** Permiten conectar el bloque prefijo `(01 | 10)*`, el infijo obligatorio `(00 | 11)` y el sufijo `(01 | 10)*` sin consumir caracteres de la cadena de entrada[cite: 2].
- **Bifurcación de alternativas:** Se ubican en las uniones de las ramas (`OR`) para permitir que la máquina intente reconocer múltiples patrones en paralelo desde un mismo punto de partida[cite: 2].
- **Construcción de Thompson:** Facilitan el retorno a estados iniciales en las clausuras de Kleene (`*`) sin introducir dependencias de símbolos adicionales[cite: 2].

---

### 2. Cálculo de la $\lambda$-clausura ($\lambda$-closure)

La **$\lambda$-clausura** de un estado $q$ representa el conjunto de todos los estados a los que se puede transitar desde $q$ utilizando únicamente transiciones vacías ($\lambda$), incluyendo al propio estado $q$[cite: 2].

A continuación se presenta el cálculo formal de la $\lambda$-clausura para el autómata del **Ejercicio 238**:

| Estado ($q$) | $\lambda$-clausura ($E(q)$) | Explicación del Alcance |
| :--- | :--- | :--- |
| **$q_0$** | $\{q_0, q_1, q_3\}$ | Desde el inicio se alcanzan por $\lambda$ los puntos de partida de las ramas no deterministas[cite: 2]. |
| **$q_1$** | $\{q_1\}$ | No posee salidas $\lambda$; requiere consumir el símbolo '0'[cite: 2]. |
| **$q_2$** | $\{q_2, q_0, q_1, q_3\}$ | Retorna al estado $q_0$ en bucle y propaga la clausura de $q_0$[cite: 2]. |
| **$q_3$** | $\{q_3\}$ | No posee salidas $\lambda$; requiere consumir el símbolo '1'[cite: 2]. |
| **$q_4$** | $\{q_4, q_0, q_1, q_3\}$ | Retorna a $q_0$ tras completar el bloque alternativo `10`[cite: 2]. |
| **$q_5$** | $\{q_5, q_6, q_8\}$ | Estado de aceptación que distribuye por $\lambda$ hacia el bloque final del sufijo[cite: 2]. |

---

### 3. Papel de la $\lambda$-clausura en el Reconocimiento de Cadenas
La $\lambda$-clausura es indispensable en la evaluación de cadenas dentro de un AFND-$\lambda$ porque[cite: 2]:
1. **Punto de partida expandido:** Permite que la simulación inicie de forma simultánea en una "superposición de estados" (todos los pertenecientes a $\lambda$-clausura($q_0$))[cite: 2].
2. **Evaluación Instantánea:** Tras consumir cada símbolo del alfabeto, la máquina recalcula la $\lambda$-clausura de los nuevos estados alcanzados antes de procesar el siguiente carácter[cite: 2].
3. **Criterio de Aceptación:** Una cadena es aceptada si al finalizar la lectura de todos sus caracteres, la interacción de la $\lambda$-clausura del conjunto actual de estados incluye al menos un estado clasificado como final (`Final State`)[cite: 2].

## 2.4. Conversiones y análisis comparativo

### 1. Metodología de Conversión
Para transformar los autómatas con transiciones nulas (AFND-$\lambda$) a Autómatas Finitos Deterministas (AFD) equivalentes en JFLAP, se sigue el procedimiento formal de dos etapas[cite: 1, 2]:
1. **Paso 1 (AFND-$\lambda \rightarrow$ AFND):** Se calcula la $\lambda$-clausura para eliminar las transiciones vacías y redefinir la función de transición sobre los símbolos de entrada $\Sigma = \{0, 1\}$[cite: 1, 2].
2. **Paso 2 (AFND $\rightarrow$ AFD):** Se aplica la construcción de subconjuntos (*Subset Construction*) mediante la opción `Convert -> Convert to DFA` de JFLAP, asignando un nuevo estado en el AFD para cada subconjunto activo alcanzible de estados del AFND[cite: 1, 2].

Los autómatas resultantes de la conversión se encuentran guardados en el directorio `automatas/conversiones/`[cite: 3].

---

### 2. Tabla Comparativa de Estados y Cota Teórica $2^n$

A continuación se analizan 5 casos representativos de la **Lista 3** comparando el número de estados en el autómata no determinista original ($n$), el número de estados en el AFD resultante y el límite teórico máximo posible ($2^n$)[cite: 1, 2]:

| Ejercicio | Expresión Regular | Estados AFND-λ ($n$) | Estados AFD Resultante | Cota Máxima Teórica ($2^n$) | ¿Alcanza la cota? |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **151** | `(00 \| 11)* (0 \| 1)*` | 6 | 4 | $2^6 = 64$ | No |
| **237** | `(0011 \| 1100)* (0 \| 1)* (0011 \| 1100)*` | 18 | 8 | $2^{18} = 262,144$ | No |
| **238** | `(01 \| 10)* (00 \| 11) (01 \| 10)*` | 9 | 6 | $2^9 = 512$ | No |
| **254** | `(00 \| 11)* (0101 \| 1010) (00 \| 11)*` | 16 | 10 | $2^{16} = 65,536$ | No |
| **260** | `(00 \| 11)* (010 \| 101) (00 \| 11)*` | 15 | 9 | $2^{15} = 32,768$ | No |

---

### 3. Explicación de la Cota $2^n$ y Caso Bibliográfico de Peor Escenario

#### Explicación Teórica de la Cota $2^n$:
La cota $2^n$ proviene del **conjunto potencia** del conjunto de estados del AFND ($\vert{}P(Q)\vert{} = 2^{\vert{}Q\vert{}}$)[cite: 1, 2]. Teóricamente, un AFD equivalente podría requerir un estado distinto por cada combinación posible de estados en los que el AFND puede encontrarse simultáneamente[cite: 1, 2].

Sin embargo, en las expresiones regulares cotidianas y de uso habitual **esta cota rara vez se alcanza**[cite: 1, 2]. Esto ocurre porque la mayoría de las combinaciones de estados son inalcanzables en la práctica debido a las restricciones de orden y estructura linealimpuestas por los lenguajes[cite: 1, 2].

#### Familia de Lenguajes donde SÍ se Alcanza la Cota Exponencial:
De acuerdo con la bibliografía clásica de Teoría de la Computación (*Hopcroft, Motwani & Ullman*), existe una familia explícita de lenguajes regulares que evidencia la explosión de estados del AFD[cite: 1, 2]:

$$L_k = \{ w \in \{0, 1\}^* \mid \text{el } k\text{-ésimo símbolo desde el final de } w \text{ es un '1'} \}$$

- **Para el AFND:** Solo requiere **$k + 1$ estados**, ya que el no determinismo le permite "adivinar" sin costo el momento exacto en que comienza el sufijo final de longitud $k$[cite: 1, 2].
- **Para el AFD:** Requiere obligatoriamente **$2^k$ estados**, debido a que un autómata determinista necesita recordar exactamente todos los combinaciones de los últimos $k$ bits leídos para no cometer errores de aceptación[cite: 1, 2].

---

### 4. Comparativa de Eficiencia y Diseño

- **Facilidad de Diseño e Interpretación:** El AFND-$\lambda$ es mucho más intuitivo y directo de diseñar a partir de expresiones regulares complejas mediante algoritmos modulares (como el de Thompson)[cite: 1, 2].
- **Eficiencia en la Ejecución/Reconocimiento:** El AFD es significativamente más eficiente en tiempo de ejecución ($O(\vert{}w\vert{})$) ya que solo requiere procesar un único estado por carácter sin necesidad de mantener ni simular bifurcaciones o calcular $\lambda$-clausuras[cite: 1, 2].
