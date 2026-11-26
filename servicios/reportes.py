"""Exportación de reportes CSV con encabezados claros y unidades."""
import csv
import io
from datetime import datetime

from calculadora.excepciones import ReporteError
from config import DIR_REPORTES
from servicios.logs import obtener_logger
from utilidades.decoradores import registrar_operacion

log = obtener_logger("reportes")

ENCABEZADOS = [
    "ID", "Fecha y hora", "Tensión (V)", "Resistencia de carga (Ω)", "Material",
    "Longitud de ida (m)", "Sección (mm²)", "Rc cable (Ω)", "Rt total (Ω)",
    "Corriente I (A)", "Caída Vc (V)", "Potencia Pc (W)",
]


def registro_a_fila(registro: dict, decimales: int = 4) -> list:
    """Convierte un registro del historial en una fila (redondea solo al presentar)."""
    e, r = registro["entradas"], registro["resultados"]
    f = lambda x: f"{x:.{decimales}f}"
    return [registro["id"], registro["fecha_hora"], f(e["tension"]), f(e["resistencia_carga"]),
            e["material"], f(e["longitud_ida"]), f(e["seccion_mm2"]), f(r["rc_ohm"]),
            f(r["rt_ohm"]), f(r["corriente_a"]), f(r["caida_tension_v"]), f(r["potencia_cable_w"])]


def _escribir(registros: list, destino) -> None:
    escritor = csv.writer(destino)
    escritor.writerow(ENCABEZADOS)
    for registro in registros:
        escritor.writerow(registro_a_fila(registro))


def csv_en_bytes(registros: list) -> bytes:
    """CSV en memoria (para el botón de descarga). utf-8-sig para que Excel lea Ω y ²."""
    if not registros:
        raise ReporteError("No hay registros para exportar.")
    buffer = io.StringIO()
    _escribir(registros, buffer)
    return buffer.getvalue().encode("utf-8-sig")


@registrar_operacion
def exportar_csv(registros: list, directorio=DIR_REPORTES):
    """Guarda el CSV en reportes/ y devuelve la ruta."""
    if not registros:
        log.warning("exportación cancelada: no hay registros")
        raise ReporteError("No hay registros para exportar.")
    ruta = directorio / f"reporte_{datetime.now():%Y%m%d_%H%M%S}.csv"
    try:
        directorio.mkdir(parents=True, exist_ok=True)
        with open(ruta, "w", newline="", encoding="utf-8-sig") as archivo:
            _escribir(registros, archivo)
    except OSError as error:
        log.error("error al exportar CSV | %s", error)
        raise ReporteError(f"No se pudo exportar: {error}") from error
    log.info("exportación correcta | archivo=%s registros=%d", ruta.name, len(registros))
    return ruta
