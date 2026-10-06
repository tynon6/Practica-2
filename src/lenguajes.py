import itertools

def prefijos(cadena: str) -> list[str]:
    """Calcula todos los prefijos de una cadena."""
    return [cadena[:i] for i in range(len(cadena) + 1)]

def sufijos(cadena: str) -> list[str]:
    """Calcula todos los sufijos de una cadena."""
    return [cadena[i:] for i in range(len(cadena) + 1)]

def subcadenas(cadena: str) -> list[str]:
    """Calcula todas las subcadenas únicas conservando el orden."""
    resultado = []
    n = len(cadena)
    for i in range(n + 1):
        for j in range(i, n + 1):
            sub = cadena[i:j]
            if sub not in resultado:
                resultado.append(sub)
    return resultado

def kleene_y_positiva(alfabeto: list[str], max_len: int) -> tuple[list[str], list[str]]:
    """Calcula Σ* y Σ+ hasta una longitud dada."""
    k = len(alfabeto)
    if k == 1:
        total = max_len + 1
    elif k > 1:
        total = (k**(max_len + 1) - 1) // (k - 1)
    else:
        total = 1

    if total > 200_000:
        raise ValueError(f"La combinación generaría {total:,} cadenas, superando el límite de 200,000.")

    sigma_estrella = []
    for l in range(max_len + 1):
        for p in itertools.product(alfabeto, repeat=l):
            sigma_estrella.append("".join(p))

    sigma_mas = [c for c in sigma_estrella if c != ""]
    return sigma_estrella, sigma_mas