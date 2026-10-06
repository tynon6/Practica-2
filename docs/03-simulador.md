# Ejercicio 3. Simulador de autómatas con interfaz gráfica

## Alcance

El simulador separa el núcleo (`src/automata.py`), los formatos (`src/formatos.py`), el dibujo (`src/visualizacion.py`) y la interfaz Flet (`src/app.py`). El núcleo y la lectura de archivos no importan Flet.

## Definición

En la interfaz se especifican alfabeto, estados, estado inicial, estados finales y transiciones. Las transiciones se escriben como `q0, a -> q1`; para no determinismo se pueden separar varios destinos con coma. Se aceptan `λ`, `ε` o `lambda` para la transición vacía. Después de definir el autómata se muestra su diagrama y una tabla editable de transiciones.

## Formatos

Se leen y se escriben `.jff`, `.json` y `.xml`. El JSON y el XML siguen la estructura del Anexo 3 de la práctica. En JFLAP, una transición lambda usa `<read/>` vacío. Las coordenadas JFLAP se toleran al importar y se generan al exportar; el modelo formal no depende de ellas.

## Simulación

La aplicación mantiene el AFND como conjunto de estados activos y calcula la λ-clausura al inicio y después de cada símbolo. Así explora todos los caminos posibles sin convertir a AFD. La cantidad de configuraciones simultáneas puede crecer hasta el número de estados; determinizar primero puede producir hasta `2ⁿ` estados. La traza muestra el conjunto de estados, las transiciones consumidas y las transiciones λ recorridas en cada clausura. Puede verse paso a paso o completa y reiniciarse para ingresar otra cadena.

## Pruebas y uso

Las pruebas de `tests/test_automata.py` comprueban las importaciones y exportaciones inversas de los tres formatos, aceptación y rechazo en un AFD, y una aceptación AFND-λ que necesita la λ-clausura. Las operaciones de prefijos, sufijos, subcadenas y cerraduras reutilizan `src/lenguajes.py` de la Práctica 1.

```powershell
python -m pip install -r requirements.txt
pytest -q
python src/app.py
```

En la interfaz se puede cambiar la definición manualmente, importar una ruta de archivo y exportar indicando su ruta y extensión. La ventana muestra la representación gráfica, tabla completa, resultado y traza paso a paso, además de las operaciones de lenguajes.
