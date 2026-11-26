"""Ejecuta las 6 pruebas mínimas del enunciado y deja evidencia en data/historial.json y logs/app.log.

Uso:  python pruebas_minimas.py
Genera la tabla 'esperado vs obtenido' para el informe.
"""
from calculadora.calculos import calcular_circuito
from calculadora.excepciones import ErrorDeValidacion
from calculadora.validaciones import validar_entradas
from servicios.historial import cargar_historial, guardar_calculo, inicializar_historial
from servicios.logs import configurar_logger, obtener_logger

configurar_logger()
log = obtener_logger("pruebas")
inicializar_historial()
filas = []


def ejecutar(entradas):
    datos = validar_entradas(*entradas)
    resultados = calcular_circuito(**datos)
    guardar_calculo(datos, resultados)
    return resultados


def rechazado(entradas):
    try:
        ejecutar(entradas)
        return "ERROR: se aceptó un dato inválido"
    except ErrorDeValidacion as e:
        return f"Rechazado -> {e}"


log.info("inicio de pruebas mínimas")
r1 = ejecutar(("12", "10", "cobre", "5", "2,5 mm²"))
filas.append(("1 Referencia", "Rc≈0,0672 Ω; I≈1,1920 A", f"Rc={r1['rc_ohm']:.4f} Ω; I={r1['corriente_a']:.4f} A"))
r2 = ejecutar(("12", "10", "aluminio", "5", "2,5 mm²"))
filas.append(("2 Material", "Resultados distintos (aluminio)", f"Rc={r2['rc_ohm']:.4f} Ω; I={r2['corriente_a']:.4f} A"))
mayor = ejecutar(("12", "10", "cobre", "5", "6"))
menor = ejecutar(("12", "10", "cobre", "5", "1"))
filas.append(("3 Sección", "Mayor sección -> menor Rc", f"6 mm²: {mayor['rc_ohm']:.4f} Ω | 1 mm²: {menor['rc_ohm']:.4f} Ω"))
filas.append(("4 Formato inválido", "Mensaje claro + WARNING", rechazado(("12", "10", "cobre", "5", "2.5 cm2"))))
filas.append(("4b Texto en campo", "Mensaje claro + WARNING", rechazado(("abc", "10", "cobre", "5", "2.5"))))
filas.append(("5 Valor no válido (cero)", "Rechazar e indicar dato", rechazado(("12", "0", "cobre", "5", "2.5"))))
filas.append(("5b Valor no válido (negativo)", "Rechazar e indicar dato", rechazado(("12", "10", "cobre", "-5", "2.5"))))
total = len(cargar_historial())
filas.append(("6 Persistencia", "Cálculos en JSON y eventos en app.log", f"{total} cálculos en data/historial.json"))
log.info("fin de pruebas mínimas | registros_en_historial=%d", total)

for nombre, esperado, obtenido in filas:
    print(f"{nombre:32} | {esperado:38} | {obtenido}")
