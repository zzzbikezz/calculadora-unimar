"""Validación y normalización de entradas.

Reglas: solo números finitos > 0; se admite coma o punto decimal.
Los campos llegan como TEXTO (para poder rechazar vacíos, letras, NaN, inf).

REGEX documentadas
------------------
PATRON_NUMERO  : ^[+-]?(\\d+([.,]\\d+)?|[.,]\\d+)$
  Admite : 12  |  2.5  |  2,5  |  .5  |  -3 (se rechaza luego por ser <= 0)
  Rechaza: ""  |  abc  |  1,000.5  |  2,5,3  |  1e3  |  nan  |  inf

PATRON_SECCION : número + unidad OPCIONAL (mm2, mm², mm^2), sin distinguir mayúsculas
  Admite : 2.5  |  2,5  |  2.5 mm2  |  2,5 mm²  |  2.5MM2
  Rechaza: 2.5 cm2  |  2.5 mm  |  AWG 12  |  dos mm2  |  2,5 mm3
"""
import math
import re

from calculadora.excepciones import ErrorDeValidacion
from calculadora.materiales import MATERIALES
from utilidades.decoradores import registrar_operacion

PATRON_NUMERO = re.compile(r"^[+-]?(\d+([.,]\d+)?|[.,]\d+)$")
PATRON_SECCION = re.compile(
    r"^\s*(?P<valor>[+-]?(?:\d+(?:[.,]\d+)?|[.,]\d+))\s*(?:mm2|mm²|mm\^2)?\s*$",
    re.IGNORECASE,
)
_NO_FINITOS = {"nan", "inf", "+inf", "-inf", "infinity", "+infinity", "-infinity"}


def _a_float_positivo(texto_numero: str, campo: str) -> float:
    """Convierte '2,5' -> 2.5 y verifica que sea finito y mayor que cero."""
    try:
        valor = float(texto_numero.replace(",", "."))
    except ValueError:
        raise ErrorDeValidacion(campo, "no es un número válido.")
    if not math.isfinite(valor):  # captura overflow (ej. 999...9 con 400 dígitos)
        raise ErrorDeValidacion(campo, "no puede ser NaN ni infinito.")
    if valor <= 0:
        raise ErrorDeValidacion(campo, "debe ser mayor que cero. Corrija este dato.")
    return valor


def validar_numero(texto, campo: str) -> float:
    """Valida un campo numérico escrito como texto."""
    if texto is None or not str(texto).strip():
        raise ErrorDeValidacion(campo, "no puede estar vacío.")
    limpio = str(texto).strip()
    if limpio.lower() in _NO_FINITOS:
        raise ErrorDeValidacion(campo, "no puede ser NaN ni infinito.")
    if not PATRON_NUMERO.match(limpio):
        raise ErrorDeValidacion(campo, "debe ser un número (use punto o coma decimal, sin letras).")
    return _a_float_positivo(limpio, campo)


def validar_seccion(texto, campo: str = "Sección transversal (mm²)") -> float:
    """Valida la sección con regex: acepta 2.5, 2,5, 2.5 mm2 y 2,5 mm²."""
    if texto is None or not str(texto).strip():
        raise ErrorDeValidacion(campo, "no puede estar vacía.")
    coincidencia = PATRON_SECCION.match(str(texto))
    if coincidencia is None:
        raise ErrorDeValidacion(
            campo, "formato no admitido. Use por ejemplo 2.5, 2,5, 2.5 mm2 o 2,5 mm² (no AWG, radio ni diámetro)."
        )
    return _a_float_positivo(coincidencia.group("valor"), campo)


def validar_material(material) -> str:
    if material not in MATERIALES:
        raise ErrorDeValidacion("Material", "seleccione cobre, aluminio u otro material de la lista.")
    return material


@registrar_operacion
def validar_entradas(tension, resistencia_carga, material, longitud_ida, seccion) -> dict:
    """Valida los cinco parámetros. Devuelve un diccionario con valores float limpios."""
    return {
        "tension": validar_numero(tension, "Tensión (V)"),
        "resistencia_carga": validar_numero(resistencia_carga, "Resistencia de carga (Ω)"),
        "material": validar_material(material),
        "longitud_ida": validar_numero(longitud_ida, "Longitud de ida (m)"),
        "seccion_mm2": validar_seccion(seccion),
    }
