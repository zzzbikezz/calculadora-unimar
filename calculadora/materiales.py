"""Resistividades de referencia a 20 °C (Ω·m). Valores aproximados y constantes.

Se guardan en un DICCIONARIO: la clave es el nombre del material y el valor
su resistividad. La interfaz solo ofrece estas claves (selector fijo).
"""
from calculadora.excepciones import ErrorDeValidacion

MATERIALES = {
    "cobre": 1.68e-8,      # obligatorio (enunciado)
    "aluminio": 2.65e-8,   # obligatorio (enunciado)
    "plata": 1.59e-8,      # adicional
    "hierro": 9.71e-8,     # adicional
}


def listar_materiales() -> list:
    """Devuelve la lista de nombres de materiales disponibles."""
    return list(MATERIALES.keys())


def obtener_resistividad(material: str) -> float:
    """Devuelve ρ (Ω·m) del material. Lanza ErrorDeValidacion si no existe."""
    if material not in MATERIALES:  # condicional de validación
        raise ErrorDeValidacion(
            "Material", f"'{material}' no es válido. Elija: {', '.join(MATERIALES)}."
        )
    return MATERIALES[material]
