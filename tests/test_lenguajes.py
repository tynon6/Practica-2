import pytest
from src.lenguajes import prefijos, sufijos, subcadenas, kleene_y_positiva

def test_cadena_vacia():
    assert prefijos("") == [""]
    assert sufijos("") == [""]
    assert subcadenas("") == [""]

def test_alfabeto_un_simbolo():
    estrella, mas = kleene_y_positiva(["a"], 3)
    assert estrella == ["", "a", "aa", "aaa"]
    assert mas == ["a", "aa", "aaa"]

def test_prefijos_sufijos_longitud_1():
    assert prefijos("x") == ["", "x"]
    assert sufijos("x") == ["x", ""]

def test_diferencia_estrella_y_mas_longitud_cero():
    estrella, mas = kleene_y_positiva(["a", "b"], 0)
    assert estrella == [""]
    assert mas == []
    assert len(estrella) - len(mas) == 1