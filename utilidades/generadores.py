"""Generadores propios (funciones con yield): recorren datos de a uno, sin cargar todo en memoria."""
from collections import deque
from datetime import datetime


def leer_lineas_log(ruta):
    """Generador: entrega las líneas de un archivo .log una por una."""
    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            yield linea.rstrip("\n")


def ultimas_lineas_log(ruta, cantidad=100, niveles=None):
    """Devuelve las últimas `cantidad` líneas (más reciente primero), con filtro opcional de nivel.

    Usa el generador leer_lineas_log y un deque de tamaño fijo.
    """
    recientes = deque(maxlen=cantidad)
    for linea in leer_lineas_log(ruta):
        partes = linea.split(" | ")
        if niveles and (len(partes) < 2 or partes[1] not in niveles):
            continue
        recientes.append(linea)
    return list(reversed(recientes))


def iterar_registros(registros, material=None, desde=None, hasta=None):
    """Generador: entrega solo los registros del historial que cumplen los filtros.

    material: nombre o None | desde/hasta: objetos datetime.date o None.
    """
    for registro in registros:  # ciclo para recorrer registros
        if material and registro.get("entradas", {}).get("material") != material:
            continue
        if desde or hasta:
            try:
                fecha = datetime.strptime(registro["fecha_hora"], "%Y-%m-%d %H:%M:%S").date()
            except (KeyError, ValueError):
                continue  # registro con fecha dañada: se omite
            if desde and fecha < desde:
                continue
            if hasta and fecha > hasta:
                continue
        yield registro
