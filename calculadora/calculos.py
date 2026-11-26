"""Lógica matemática del circuito DC en serie. NO depende de Streamlit.

Orden obligatorio del enunciado:
  1) A(m²)=A(mm²)·1e-6   2) Ltotal=2·L   3) Rc=ρ·Ltotal/A   4) Rt=Rcarga+Rc
  5) I=V/Rt              6) Vc=I·Rc      7) Pc=I²·Rc
No se redondea nada aquí: el redondeo ocurre solo al presentar.
"""
from calculadora.excepciones import ErrorDeValidacion
from calculadora.materiales import obtener_resistividad
from utilidades.decoradores import registrar_operacion


# ---------------------------------------------------------------- fórmulas
def convertir_mm2_a_m2(area_mm2: float) -> float:
    return area_mm2 * 1e-6


def calcular_longitud_total(longitud_ida: float) -> float:
    return 2 * longitud_ida


def calcular_resistencia_cable(rho: float, longitud_total: float, area_m2: float) -> float:
    return rho * longitud_total / area_m2


def calcular_resistencia_total(resistencia_carga: float, resistencia_cable: float) -> float:
    return resistencia_carga + resistencia_cable


def calcular_corriente(tension: float, resistencia_total: float) -> float:
    return tension / resistencia_total


def calcular_caida_tension(corriente: float, resistencia_cable: float) -> float:
    return corriente * resistencia_cable


def calcular_potencia_cable(corriente: float, resistencia_cable: float) -> float:
    return corriente ** 2 * resistencia_cable


# ------------------------------------------------------- función principal
@registrar_operacion
def calcular_circuito(tension, resistencia_carga, material, longitud_ida, seccion_mm2) -> dict:
    """Calcula todas las magnitudes. Devuelve un diccionario SIN redondear."""
    for nombre, valor in (("Tensión", tension), ("Resistencia de carga", resistencia_carga),
                          ("Longitud", longitud_ida), ("Sección", seccion_mm2)):
        if valor <= 0:  # defensa extra: la lógica no confía ciegamente en la interfaz
            raise ErrorDeValidacion(nombre, "debe ser mayor que cero.")

    rho = obtener_resistividad(material)
    area_m2 = convertir_mm2_a_m2(seccion_mm2)                       # 1
    longitud_total = calcular_longitud_total(longitud_ida)          # 2
    rc = calcular_resistencia_cable(rho, longitud_total, area_m2)   # 3
    rt = calcular_resistencia_total(resistencia_carga, rc)          # 4
    i = calcular_corriente(tension, rt)                             # 5
    vc = calcular_caida_tension(i, rc)                              # 6
    pc = calcular_potencia_cable(i, rc)                             # 7
    return {
        "rc_ohm": rc,
        "rt_ohm": rt,
        "corriente_a": i,
        "caida_tension_v": vc,
        "potencia_cable_w": pc,
    }


# ------------------------------------------------------------ presentación
def formatear_resultados(resultados: dict, decimales: int = 4) -> list:
    """Redondea SOLO al presentar. Devuelve [(símbolo, valor_texto, unidad, significado)]."""
    definicion = [
        ("Rc", "rc_ohm", "Ω", "Resistencia del cable de ida y retorno."),
        ("Rt", "rt_ohm", "Ω", "Resistencia total del circuito en serie: carga + cable."),
        ("I", "corriente_a", "A", "Corriente estimada que circula por la carga y el conductor."),
        ("Vc", "caida_tension_v", "V", "Tensión que cae en el cable (no es la tensión de la carga)."),
        ("Pc", "potencia_cable_w", "W", "Potencia disipada en el cable (no es la de la carga)."),
    ]
    return [(sim, f"{resultados[clave]:.{decimales}f}", unidad, texto)
            for sim, clave, unidad, texto in definicion]
