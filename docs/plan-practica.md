# Análisis y plan de la Práctica 2

La práctica tiene cinco ejercicios. Este repositorio desarrolla el Ejercicio 3; los demás quedan como trabajo pendiente del alumno.

## Dependencias entre ejercicios

1. **Entorno y ramas:** reutilizar Docker/Compose, dependencias, pruebas y el módulo de lenguajes de la Práctica 1; trabajar por funcionalidad, usar Pull Requests y configurar CI para Python 3.11, 3.12 y 3.13.
2. **AFND/AFND-λ en JFLAP:** completar ejercicios 94–263 de las Listas 2 y 3 (conservar los de Práctica 1), clasificarlos y documentar diez cadenas por autómata, λ-clausuras y conversiones. Es el bloque más extenso y requiere trabajar con el material de las listas.
3. **Simulador:** definir, visualizar, importar, simular, exportar autómatas y reutilizar las operaciones anteriores. Está preparado en este repositorio.
4. **Investigación:** documento de 3–5 cuartillas sobre no determinismo, λ-clausura, construcción de subconjuntos, cota 2ⁿ, Kleene y Myhill–Nerode/Hopcroft; análisis del artículo asignado y dos artículos arbitrados nuevos con DOI.
5. **Del artículo al autómata:** escoger una aplicación de la literatura, formalizarla, producir un `.jff`, validarla en el simulador y documentar al menos diez cadenas y los límites de la abstracción.

## Ruta sugerida

Primero completar el punto 3 y usarlo con los autómatas que se construyan en el punto 2; luego documentar conversiones y evidencias del punto 2; después preparar la investigación del punto 4 y elegir desde ahí el sistema para el punto 5. Mantener el historial con una rama y un Pull Request por funcionalidad y no fusionar cambios que aún no pasen pruebas.

## Material faltante detectado

- La Práctica 1 entregada en `tynon6/Practica-1` tiene `src/lenguajes.py`, `test/test_lenguajes.py`, `entorno/compose.yml` y `entorno/dockerfile`; se reutilizaron los módulos y el entorno.
- No hay `pytest.ini` en la Práctica 1.
- No hay un `requirements.txt` en la raíz de la Práctica 1. Sí existe `entorno/requirements.txt`, pero está vacío. En este repositorio se creó un `requirements.txt` fijado con Flet, Pillow y pytest, además del `pytest.ini` requerido para que pytest encuentre el código en `src/`.
- Para resolver el Ejercicio 2 hacen falta las Listas 2 y 3 completas, que no vienen adjuntas aquí. El artículo del Ejercicio 4.2 está identificado por DOI en el PDF; los dos artículos nuevos también deben investigarse y verificarse antes de redactar esa sección.

## Requisitos de cierre del repositorio

El punto 3 no sustituye los ejercicios 1, 2, 4 y 5. La práctica completa todavía requiere sus documentos Markdown, autómatas JFLAP, conversiones, registros de Pull Requests, cuatro o más ramas fusionadas, evidencias de CI, referencias académicas APA 7 y permiso de lectura al docente si el repositorio continúa privado.
