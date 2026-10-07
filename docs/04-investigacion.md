# Ejercicio 4. Investigación y estado del arte

Práctica 2: Autómatas Finitos No Deterministas (AFND) y Simulación de AFD con Interfaz Gráfica
Teoría de la Computación, ESCOM-IPN

[Volver al índice](../README.md)

**Fuentes.** Todo lo que sigue se sustenta en libros con ISBN, artículos con DOI, la documentación oficial citada con fecha de acceso y el artículo original de Rabin y Scott (1959). Para las definiciones y los algoritmos se emplean Sipser (2013) y Hopcroft et al. (2007); si el libro de texto de su grupo es otro, sustituya las referencias de capítulo por las equivalentes. Los números de la tabla de la sección 4.1.4 son un cálculo propio con un script de referencia (subconjuntos alcanzables y minimización por refinamiento de particiones), no una cita.

## Índice

- [4.1 Investigación](#41-investigación)
- [4.2 Artículo asignado: Rabin y Scott (1959)](#42-artículo-asignado-rabin-y-scott-1959)
- [4.3 Dos artículos localizados](#43-dos-artículos-localizados)
- [Referencias](#referencias)

---

## 4.1 Investigación

### 4.1.1 El no determinismo: AFN y AFN-λ

Un AFD es una quíntupla (Q, Σ, δ, q₀, F) con δ : Q × Σ → Q. En cada paso hay exactamente una transición posible (Sipser, 2013, sección 1.1). En un autómata no determinista, una configuración puede tener varias transiciones, o ninguna, para el mismo símbolo.

- **AFN estándar:** (Q, Σ, δ, q₀, F) con δ : Q × Σ → 𝒫(Q). Cada par (estado, símbolo) lleva a un *conjunto* de estados, posiblemente vacío.
- **AFN-λ:** igual, pero con δ : Q × (Σ ∪ {λ}) → 𝒫(Q). Una transición con λ se toma sin leer ningún símbolo (Hopcroft et al., 2007, sección 2.5).

Rabin y Scott (1959, Definición 9) definen el AFN con un *conjunto* de estados iniciales S₀ ⊆ S, y no incluyen transiciones λ, que son una extensión posterior de la literatura.

**Qué significa que una cadena sea aceptada.** Un AFN no es una máquina probabilística, sino una máquina con varias opciones en cada movimiento. Una cadena w = a₁…aₙ es aceptada si *existe al menos una* secuencia de estados s₀, s₁, …, sₙ con s₀ el inicial, sᵢ ∈ δ(sᵢ₋₁, aᵢ) y sₙ ∈ F (Rabin y Scott, 1959, Definición 10). Los caminos que se bloquean o terminan en un estado no final se descartan. La cadena se rechaza solo si *ningún* camino acepta. En el AFN-λ, la definición admite además cualquier número de transiciones λ entre un símbolo y el siguiente. Con la función extendida δ̂, w es aceptada si δ̂(q₀, w) ∩ F ≠ ∅ (Hopcroft et al., 2007, sección 2.5).

### 4.1.2 La λ-clausura

**Definición.** La λ-clausura de un estado q, λ-clausura(q), es el conjunto de estados alcanzables desde q siguiendo cero o más transiciones λ. Siempre contiene a q. Para un conjunto S, λ-clausura(S) es la unión de las clausuras de sus elementos (Hopcroft et al., 2007, sección 2.5).

**Algoritmo.** Es una búsqueda en el grafo formado solo por las transiciones λ:

```text
λ-clausura(S):
    R ← S ;  pila ← S
    mientras pila no esté vacía:
        q ← sacar(pila)
        para cada p en δ(q, λ):
            si p ∉ R:  R ← R ∪ {p} ;  meter(pila, p)
    devolver R
```

Su costo es lineal en el número de estados y de transiciones λ. Con ella se define δ̂(q, λ) = λ-clausura({q}) y δ̂(q, wa) = λ-clausura(⋃ₚ∈δ̂(q,w) δ(p, a)). La clausura es lo que permite aceptar cadenas "gratis".

**Ejemplo (el AFN-λ del Anexo 3 de la práctica).** Con q₀ –a→ q₁, q₀ –b→ q₀, q₀ –λ→ q₁ y F = {q₁}: λ-clausura(q₀) = {q₀, q₁} y λ-clausura(q₁) = {q₁}. Como la clausura del estado inicial contiene a un estado final, la cadena vacía es aceptada sin leer nada. El lenguaje reconocido es b\*(a + λ), lo que se comprobó por enumeración de todas las cadenas de longitud menor o igual que 7.

### 4.1.3 La construcción de subconjuntos

**Teorema (equivalencia AFD–AFN).** Para todo AFN (o AFN-λ) N existe un AFD D con L(D) = L(N). Rabin y Scott (1959, Teorema 11) lo demuestran por primera vez; en Sipser (2013, sección 1.2) y Hopcroft et al. (2007, sección 2.3) aparece como el teorema estándar.

**Construcción.** Dado N = (Q, Σ, δ, q₀, F), se define D = (Q_D, Σ, δ_D, q_D, F_D) con:

- Q_D ⊆ 𝒫(Q) (en la práctica, solo los subconjuntos *alcanzables*);
- q_D = λ-clausura({q₀});
- δ_D(S, a) = λ-clausura(⋃ₚ∈S δ(p, a));
- F_D = {S ∈ Q_D | S ∩ F ≠ ∅}.

Rabin y Scott toman Q_D = 𝒫(S), N(t, σ) = ⋃ₛ∈t M(s, σ) y G = los subconjuntos que contienen al menos un elemento de F (Definición 11).

**Esbozo de la demostración.** Se prueba por inducción sobre |w| que δ̂_D(q_D, w) = δ̂_N(q₀, w), es decir, que el estado de D tras leer w es *exactamente* el conjunto de estados en que puede estar N. Para |w| = 0 es la definición de q_D. Para wa se usa que δ_D aplica δ a todos los estados del conjunto y luego cierra bajo λ. Por tanto, w ∈ L(D) ⇔ δ̂_N(q₀, w) ∩ F ≠ ∅ ⇔ w ∈ L(N). Rabin y Scott lo prueban en dos inclusiones: para L(N) ⊆ L(D) muestran por inducción que cada estado de una secuencia aceptante pertenece al conjunto alcanzado; para la otra, retroceden desde un estado final del último subconjunto eligiendo, paso a paso, un predecesor.

**Ejemplo.** El AFN-λ del Anexo 3 se determiniza a 3 estados: {q₀,q₁} (inicial y final), {q₁} (final) y ∅ (muerto), con {q₀,q₁} –a→ {q₁}, {q₀,q₁} –b→ {q₀,q₁} y todas las demás transiciones hacia ∅. El subconjunto {q₀} nunca aparece, porque la clausura siempre le añade q₁.

### 4.1.4 El costo de la conversión y la cota 2ⁿ

Si N tiene n estados, D tiene como máximo 2ⁿ estados, uno por subconjunto (Rabin y Scott, 1959, Definición 11). La cota rara vez se alcanza por tres razones:

1. **Subconjuntos inalcanzables.** La construcción solo conserva los alcanzables desde el inicial. En el ejemplo anterior, de 2² = 4 posibles se generan 3.
2. **Estructura del autómata.** Un AFN sin estados finales da un AFD de un estado, y un AFN que ya es determinista da uno del mismo tamaño. Brzozowski demostró que, si el AFN es *trim* y *co-determinista*, la construcción produce directamente el AFD mínimo (citado en Baburin y Cotterell, 2025, Teorema 2).
3. **Equivalencia de estados.** Aun cuando se generen muchos subconjuntos, varios pueden ser equivalentes y colapsar al minimizar.

**Familias en las que sí se alcanza.** Moore (1971) demostró que existen AFN de n estados cuyo AFD equivalente mínimo requiere exactamente 2ⁿ estados, y otro tanto vale para el autómata de Meyer y Fischer (1971); ambos se recogen en Baburin y Cotterell (2025, sección 3). El lenguaje de Meyer–Fischer se describe allí como {xy | x ∈ {λ} ∪ {a,b}\*b, y ∈ {a,b}\*, |y|ₐ ≡ 0 (mod n)}.

Como ejemplo didáctico verificable se emplea la familia clásica **Lₙ = {w ∈ {0,1}\* | el n-ésimo símbolo desde el final de w es 1}**. Tiene un AFN de n + 1 estados: q₀ con bucles en 0 y 1, q₀ –1→ q₁ y qᵢ –0,1→ qᵢ₊₁ hasta qₙ final. Cualquier AFD necesita al menos 2ⁿ estados. Dos cadenas x e y de longitud n que difieren en la posición i se distinguen con el sufijo z = 0ⁱ⁻¹: el n-ésimo símbolo desde el final de xz es xᵢ y el de yz es yᵢ. Hay 2ⁿ cadenas de longitud n y todas son no equivalentes, de modo que el índice de la relación de Nerode es al menos 2ⁿ, y por el Corolario 2.1 de Rabin y Scott (1959) ese número es el mínimo de estados.

| n | Estados del AFN (n + 1) | Subconjuntos alcanzables | Estados del AFD mínimo | 2ⁿ |
|---|---|---|---|---|
| 1 | 2 | 2 | 2 | 2 |
| 2 | 3 | 4 | 4 | 4 |
| 3 | 4 | 8 | 8 | 8 |
| 4 | 5 | 16 | 16 | 16 |
| 5 | 6 | 32 | 32 | 32 |
| 6 | 7 | 64 | 64 | 64 |
| 7 | 8 | 128 | 128 | 128 |

(Cálculo propio.) Aquí el crecimiento exponencial es genuino: con 8 estados no deterministas, el AFD mínimo ya tiene 128. Esta familia queda un factor 2 por debajo de la cota 2ⁿ⁺¹ para n + 1 estados; las familias de Moore y de Meyer–Fischer alcanzan la cota exacta.

### 4.1.5 El teorema de Kleene

**Enunciado.** Un lenguaje es reconocido por un autómata finito si y solo si se describe con una expresión regular. Rabin y Scott (1959, Teorema 14, atribuido a Kleene y Myhill) lo formulan como: la clase de los conjuntos definibles es la menor que contiene a los conjuntos finitos y es cerrada bajo unión, producto complejo (concatenación) y cerradura. Los autores esbozan la demostración sin darla completa. Las dos direcciones se resuelven con construcciones estándar:

- **Expresión regular → autómata:** la construcción de Thompson produce un AFN-λ por inducción sobre la expresión (Hopcroft et al., 2007, sección 3.2.3).
- **Autómata → expresión regular:** por eliminación de estados (Hopcroft et al., 2007, sección 3.2.2) o con autómatas generalizados (Sipser, 2013, sección 1.3).

Con la construcción de subconjuntos, los tres modelos (AFD, AFN-λ y expresiones regulares) describen la misma clase de lenguajes, los regulares.

### 4.1.6 Minimización de un AFD

**Teorema de Myhill–Nerode.** Para un lenguaje L, la relación x ≡_L y ⇔ (∀z)(xz ∈ L ⇔ yz ∈ L) es una equivalencia invariante por la derecha. L es regular si y solo si ≡_L tiene índice finito. Rabin y Scott (1959, Teoremas 1 y 2) lo dan en su forma de Myhill y de Nerode, y en el Corolario 2.1 establecen que el número de clases es el mínimo número de estados de cualquier autómata que defina a L. El autómata cuyos estados son las clases [x], con δ([x], a) = [xa], inicial [λ] y finales las clases dentro de L, es el mínimo (demostración de (iii) ⇒ (i) del Teorema 2). La misma herramienta prueba que un lenguaje *no* es regular: para {0ⁿ10ⁿ} existen n ≠ m con 0ⁿ ≡ 0ᵐ, y entonces 0ⁿ10ᵐ estaría en el lenguaje, lo que es absurdo (Rabin y Scott, 1959, sección 2).

**Algoritmo de Hopcroft.** Calcula el AFD mínimo por refinamiento de particiones en tiempo O(|Σ| · n log n) (Berstel et al., 2008). Parte del AFD sin estados inalcanzables:

1. Partición inicial P = {F, Q \ F}.
2. La lista de trabajo W recibe, para cada símbolo a, la pareja (el menor de F y Q \ F, a).
3. Mientras W no esté vacía: se extrae (C, a). Cada bloque B de P que (C, a) *divida*, porque algunos estados de B llegan a C leyendo a y otros no, se sustituye por B′ y B″. Si (B, b) estaba en W, se reemplaza por (B′, b) y (B″, b); si no, se añade solo la pareja del *menor* de los dos.
4. Al terminar, cada bloque es un estado del AFD mínimo.

El truco de procesar siempre la mitad menor es lo que da el factor log n. El algoritmo no es del todo determinista, porque no se especifica qué pareja se extrae, pero todas las ejecuciones dan la misma partición (Berstel et al., 2008). Knuutila (2001) lo reconstruye con justificación de corrección y análisis de tiempo. El método clásico de Moore, por pares de estados distinguibles, es O(n²) en la forma más simple (Hopcroft et al., 2007, sección 4.4).

### 4.1.7 Qué significa, en la práctica, que el no determinismo no aumente el poder

Significa que **todo lo que un AFN reconoce lo reconoce también un AFD**, de modo que el no determinismo es una herramienta de *diseño y de descripción*, no de capacidad. Rabin y Scott (1959) lo aprovechan para construir con pocos estados autómatas "muy potentes" y para demostrar con rapidez las propiedades de cerradura. Las consecuencias prácticas son tres:

- **Descripción más compacta.** Un AFN puede ser exponencialmente menor que el AFD (sección 4.1.4). Conviene diseñar en AFN y convertir después.
- **Dos formas de ejecutarlo.** (a) Simular el AFN siguiendo el *conjunto de estados* posibles, con costo proporcional a |w| por el tamaño del autómata y sin crecimiento exponencial de memoria, o (b) convertirlo antes a AFD, con reconocimiento en tiempo lineal pero con riesgo de 2ⁿ estados. Predecir si la conversión explotará es PSPACE-difícil (Baburin y Cotterell, 2025).
- **El motor importa.** Un motor de expresiones regulares que explore los caminos por retroceso puede tardar un tiempo exponencial, mientras que los que simulan el conjunto de estados son lineales (Davis et al., 2018).

La igualdad de poder es una propiedad de los autómatas *finitos*. No se extiende automáticamente a otros modelos: en los autómatas de pila el no determinismo sí añade poder (Sipser, 2013, sección 2.4).

---

## 4.2 Artículo asignado: Rabin y Scott (1959)

> Rabin, M. O., y Scott, D. (1959). Finite automata and their decision problems. *IBM Journal of Research and Development, 3*(2), 114-125. https://doi.org/10.1147/rd.32.0114

### a) Dónde se prueba que todo AFN tiene un AFD equivalente

En la **sección 5, «Nondeterministic operation»** (capítulo II, «Reductions to one-way automata»), aproximadamente en las pp. 120-121 según la paginación del PDF consultado. Allí aparecen la Definición 9 (AFN), la Definición 10 (aceptación), la Definición 11 (el autómata 𝔇(𝔄) de subconjuntos) y el **Teorema 11**: T(𝔄) = T(𝔇(𝔄)).

**La construcción con la notación del curso.** Dado el AFN N = (Q, Σ, δ, q₀, F), el AFD es D = (𝒫(Q), Σ, δ_D, {q₀}, F_D), donde:

- δ_D(S, a) = ⋃ₚ∈S δ(p, a), la unión de lo que alcanza cada estado del conjunto;
- F_D = {S ⊆ Q | S ∩ F ≠ ∅}.

La demostración tiene dos inclusiones. Si w = a₀…aₙ₋₁ ∈ L(N) con la secuencia s₀, …, sₙ, por inducción sₖ ∈ δ̂_D({q₀}, a₀…aₖ₋₁), y como sₙ ∈ F el estado final de D contiene un estado de F. Recíprocamente, si D acepta w, se elige sₙ ∈ F dentro del último subconjunto y se retrocede, subconjunto a subconjunto, escogiendo en cada uno un predecesor, hasta llegar a q₀. En este artículo no hay transiciones λ, así que no aparece la clausura: esa parte de la construcción es posterior.

### b) Diferencias de notación con el libro de texto (Sipser, 2013)

| Rabin y Scott (1959) | Libro de texto |
|---|---|
| Cadena = «tape» (cinta), vacía = Λ | Cadena w, vacía = ε (en el curso, λ) |
| Conjunto de todas las cadenas: 𝒯 | Σ\* |
| Autómata 𝔄 = (S, M, s₀, F), con M la «tabla de movimientos» | M = (Q, Σ, δ, q₀, F) |
| Lenguaje = «conjunto definible», T(𝔄) | Lenguaje L(M) |
| AFN con un *conjunto* de estados iniciales S₀ ⊆ S | Un único estado inicial q₀; el AFN incluye transiciones ε |
| Aceptación como existencia de una sucesión s₀, …, sₙ | Aceptación mediante δ̂ o un árbol de cómputo |
| Extensión de M por M(s, xu) = M(M(s, x), u) | δ̂(q, wa) = δ(δ̂(q, w), a) |

**Cuál me resulta más clara.** A mi juicio, la del libro de texto para el trabajo cotidiano: el estado inicial único y las transiciones ε permiten componer autómatas por construcciones como la de Thompson, y la notación δ/δ̂ es la que usa JFLAP. De Rabin y Scott me parece más clara la *definición explícita* del autómata de subconjuntos 𝔇(𝔄) y el hecho de que, al permitir varios estados iniciales, el estado inicial de D es simplemente S₀, sin paso de clausura. Es una preferencia de lectura, no una afirmación del texto.

### c) El Premio Turing de 1976

La ACM (s. f.-a, s. f.-b) otorgó el Premio A. M. Turing de 1976 conjuntamente a Rabin y a Scott por este artículo. Su mención oficial lo reconoce porque introdujo la idea de «nondeterministic machines», un concepto que calificó de enormemente valioso, y añade que el trabajo ha sido una fuente continua de inspiración para investigaciones posteriores. La distinción, por tanto, no se justifica por un teorema aislado, sino por haber incorporado el no determinismo como concepto. La lectura del propio artículo respalda esa valoración: los autores lo emplean como «poderosa herramienta» para las pruebas de cerradura y para relacionar los autómatas de una y dos cintas (Rabin y Scott, 1959, capítulo III).

---

## 4.3 Dos artículos localizados

Ambos cuentan con DOI y fueron publicados en congresos con revisión por pares, a partir de 2018 y distintos de los cinco artículos de la Práctica 1. El primero describe una **implementación construida y medida**; el segundo es un resultado teórico directamente sobre la construcción de subconjuntos.

### Ficha A. Automata Tutor v3

**1. Cita (APA 7).** D'Antoni, L., Helfrich, M., Kretinsky, J., Ramneantu, E., y Weininger, M. (2020). Automata Tutor v3. En S. K. Lahiri y C. Wang (Eds.), *Computer aided verification: 32nd International Conference, CAV 2020, Part II* (Lecture Notes in Computer Science, Vol. 12225, pp. 3-14). Springer. https://doi.org/10.1007/978-3-030-53291-8_1

**2. Problema.** Con grupos cada vez más numerosos, corregir a mano ejercicios de autómatas y lenguajes formales y dar retroalimentación personalizada no escala. Se busca una herramienta que califique y explique los errores de forma automática y verificable.

**3. Método.** Una herramienta web (interfaz en Scala y JavaScript, servidor en C# apoyado en la biblioteca AutomataDotNet, base de datos H2) que añade doce tipos de problemas a los cuatro de la versión anterior: construcción de expresiones regulares y de autómatas de pila, conversión de expresión regular a AFN-λ paso a paso, clases de equivalencia de Myhill–Nerode, juego del lema de bombeo, entre otros. Califica con técnicas de síntesis y procedimientos de decisión, y devuelve *contraejemplos* (una cadena aceptada por un lenguaje y no por el otro). Para los lenguajes de pila, donde la equivalencia es indecidible, compara solo las cadenas hasta cierta longitud y declara que no puede afirmar que los lenguajes sean iguales.

**4. Resultado principal.** Se desplegó en 2019 en un curso de unas 950 personas: 79 problemas, 76 507 usos de retroalimentación y 26 535 correcciones manuales ahorradas al profesorado; escaló a 950 usuarios concurrentes con siete máquinas virtuales. En una encuesta (respondida por el 14.6 % del grupo) los estudiantes coincidieron en que aprendieron a usarla rápido, en que la retroalimentación fue útil y en que se sentían mejor preparados para el examen. La participación en la encuesta fue voluntaria y sin incentivo, y es una limitación de la evidencia.

**5. Relación con el temario.** Construcción de AFD y AFN, expresión regular → AFN-λ (misma construcción que Hopcroft et al., sección 3.2.3), equivalencia de estados (Myhill–Nerode) y equivalencia de lenguajes.

**6. Aportación a mi trabajo.** Es un modelo para el simulador del Ejercicio 3: verificar equivalencia devolviendo una *cadena testigo*, y distinguir la comprobación exacta (para autómatas finitos es decidible, Rabin y Scott, 1959, Teorema 10) de la acotada por longitud. También deja ver las limitaciones de JFLAP en retroalimentación, que los autores mencionan.

### Ficha B. A close analysis of the subset construction

**1. Cita (APA 7).** Baburin, I., y Cotterell, R. (2025). A close analysis of the subset construction. En *Descriptional complexity of formal systems (DCFS 2025)*. Springer. https://doi.org/10.1007/978-3-031-97100-6_2

> Complete volumen, editores y páginas desde la ficha de Springer antes de entregar.

**2. Problema.** La construcción de subconjuntos puede producir hasta 2ⁿ estados. Se pregunta si es posible *predecir* el tamaño del AFD resultante sin construirlo.

**3. Método.** Reducciones desde la universalidad de AFN (PSPACE-completa) para demostrar la dificultad de aproximar el número de estados. Después introducen la *complejidad de subconjunto* ‖A‖, una cota superior que combina el tamaño del monoide de transiciones y el rango de las matrices booleanas de transición, y la acotan con la ciclicidad y el rango.

**4. Resultado principal.** Es PSPACE-difícil calcular cualquier aproximación polinomial de la complejidad de estados de un AFN, y también decidir si la construcción de subconjuntos tendrá un crecimiento exponencial; no hay, salvo que PSPACE = P, un pronóstico eficiente. Como remedio, ‖A‖ ofrece una condición *suficiente*: si todas las matrices de transición salvo una tienen rango bajo, el AFD es de tamaño polinomial. Es un resultado teórico, sin implementación ni experimentos.

**5. Relación con el temario.** Teorema de equivalencia AFD–AFN, construcción de subconjuntos, cota 2ⁿ y minimización.

**6. Aportación a mi trabajo.** Proporciona las familias de Moore y de Meyer–Fischer para la tabla del Ejercicio 2.4, y justifica la decisión de diseño del Ejercicio 3.3: como no se puede saber de antemano si la conversión explotará, el simulador conviene que siga el conjunto de estados y fije un tope de estados si convierte a AFD.

---

## Referencias

Association for Computing Machinery. (s. f.-a). *Michael O. Rabin: A.M. Turing Award 1976*. Recuperado el 6 de octubre de 2026, de https://amturing.acm.org/award_recipient/rabin_9681074

Association for Computing Machinery. (s. f.-b). *Dana S. Scott: A.M. Turing Award 1976*. Recuperado el 6 de octubre de 2026, de https://awards.acm.org/award_winners/scott_1193622

Baburin, I., y Cotterell, R. (2025). A close analysis of the subset construction. En *Descriptional complexity of formal systems (DCFS 2025)*. Springer. https://doi.org/10.1007/978-3-031-97100-6_2

Berstel, J., Boasson, L., y Carton, O. (2008). Hopcroft's automaton minimization algorithm and Sturmian words. *DMTCS Proceedings, AI*, 351-362. https://dmtcs.episciences.org/3576

D'Antoni, L., Helfrich, M., Kretinsky, J., Ramneantu, E., y Weininger, M. (2020). Automata Tutor v3. En S. K. Lahiri y C. Wang (Eds.), *Computer aided verification: 32nd International Conference, CAV 2020, Part II* (Lecture Notes in Computer Science, Vol. 12225, pp. 3-14). Springer. https://doi.org/10.1007/978-3-030-53291-8_1

Davis, J. C., Coghlan, C. A., Servant, F., y Lee, D. (2018). The impact of regular expression denial of service (ReDoS) in practice: An empirical study at the ecosystem scale. En *Proceedings of the 2018 26th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering* (pp. 246-256). Association for Computing Machinery. https://doi.org/10.1145/3236024.3236027

Fischer, M. J., y Meyer, A. R. (1971). Economy of description by automata, grammars, and formal systems. En *Conference record 1971 twelfth annual symposium on switching and automata theory* (pp. 188-191). IEEE Computer Society.

Hopcroft, J. E., Motwani, R., y Ullman, J. D. (2007). *Introduction to automata theory, languages, and computation* (3.ª ed.). Addison-Wesley. ISBN 978-0-321-45536-9.

Knuutila, T. (2001). Re-describing an algorithm by Hopcroft. *Theoretical Computer Science, 250*(1-2), 333-363. https://doi.org/10.1016/S0304-3975(99)00150-4

Moore, F. R. (1971). On the bounds for state-set size in the proofs of equivalence between deterministic, nondeterministic, and two-way finite automata. *IEEE Transactions on Computers, C-20*(10), 1211-1214. https://ieeexplore.ieee.org/document/1671701

Rabin, M. O., y Scott, D. (1959). Finite automata and their decision problems. *IBM Journal of Research and Development, 3*(2), 114-125. https://doi.org/10.1147/rd.32.0114

Sipser, M. (2013). *Introduction to the theory of computation* (3.ª ed.). Cengage Learning. ISBN 978-1-133-18779-0.
