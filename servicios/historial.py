"""Persistencia del historial en data/historial.json (qué cálculos hizo el usuario).

Distinto de los Logs: el historial guarda DATOS del usuario; los logs guardan EVENTOS técnicos.
"""
import json
import os
from datetime import datetime

from calculadora.excepciones import HistorialError
from config import FORMATO_FECHA, RUTA_HISTORIAL
from servicios.logs import obtener_logger
from utilidades.decoradores import registrar_operacion
from utilidades.generadores import iterar_registros

log = obtener_logger("historial")


def inicializar_historial(ruta=RUTA_HISTORIAL) -> None:
    """Crea carpeta y archivo con lista vacía si no existen."""
    if ruta.exists():
        return
    log.warning("archivo de historial aún inexistente; se creará | %s", ruta.name)
    try:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump([], archivo)
    except OSError as error:
        log.error("no se pudo crear el historial | %s", error)
        raise HistorialError(f"No se pudo crear el historial: {error}") from error
    log.info("historial inicializado | %s", ruta.name)


def cargar_historial(ruta=RUTA_HISTORIAL) -> list:
    """Lee el JSON. Si está dañado lo respalda y reinicia vacío (sin cerrar la app)."""
    inicializar_historial(ruta)
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        if not isinstance(datos, list):
            raise ValueError("el JSON no contiene una lista de registros")
    except (json.JSONDecodeError, ValueError) as error:
        respaldo = ruta.with_name(f"{ruta.stem}.corrupto.{datetime.now():%Y%m%d%H%M%S}.json")
        log.error("JSON de historial corrupto; se respalda como %s | %s", respaldo.name, error)
        try:
            os.replace(ruta, respaldo)
        except OSError:
            pass
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump([], archivo)
        return []
    except OSError as error:
        log.error("error de lectura del historial | %s", error)
        raise HistorialError(f"No se pudo leer el historial: {error}") from error
    log.info("lectura correcta del historial | registros=%d", len(datos))
    return datos


def _siguiente_id(registros: list) -> str:
    numeros = [int(r["id"]) for r in registros if str(r.get("id", "")).isdigit()]
    return f"{(max(numeros) if numeros else 0) + 1:04d}"


@registrar_operacion
def guardar_calculo(entradas: dict, resultados: dict, ruta=RUTA_HISTORIAL) -> dict:
    """Agrega un cálculo exitoso al JSON y devuelve el registro creado."""
    registros = cargar_historial(ruta)
    registro = {
        "id": _siguiente_id(registros),
        "fecha_hora": datetime.now().strftime(FORMATO_FECHA),
        "entradas": dict(entradas),
        "resultados": dict(resultados),
    }
    registros.append(registro)
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(registros, archivo, ensure_ascii=False, indent=2)
    except OSError as error:
        log.error("error de escritura del historial | %s", error)
        raise HistorialError(f"No se pudo guardar el cálculo: {error}") from error
    log.info("escritura correcta del historial | id=%s", registro["id"])
    return registro


def filtrar_historial(registros: list, material=None, desde=None, hasta=None) -> list:
    """Filtra por material y/o rango de fechas usando el generador iterar_registros."""
    filtrados = list(iterar_registros(registros, material, desde, hasta))
    if not filtrados:
        log.warning("filtro sin coincidencias | material=%s desde=%s hasta=%s", material, desde, hasta)
    return filtrados
