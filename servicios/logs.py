"""Sistema de Logs con el módulo estándar logging -> logs/app.log.

Formato de cada línea:  fecha/hora | NIVEL | módulo.función | mensaje
"""
import logging

from config import (DIR_LOGS, FORMATO_FECHA, FORMATO_LOG, NOMBRE_LOGGER_BASE, RUTA_LOG)
from utilidades.generadores import ultimas_lineas_log


def configurar_logger(ruta=RUTA_LOG) -> logging.Logger:
    """Configura (una sola vez) el logger base 'calculadora'. Es seguro llamarla varias veces."""
    logger = logging.getLogger(NOMBRE_LOGGER_BASE)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    destino = str(ruta)
    ya_configurado = any(getattr(h, "baseFilename", None) == str(ruta.resolve()) for h in logger.handlers)
    if not ya_configurado:
        try:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            manejador = logging.FileHandler(destino, encoding="utf-8")
        except OSError:
            manejador = logging.StreamHandler()  # respaldo si no se puede escribir el archivo
        manejador.setFormatter(logging.Formatter(FORMATO_LOG, FORMATO_FECHA))
        logger.addHandler(manejador)
    return logger


def obtener_logger(nombre: str) -> logging.Logger:
    """Devuelve un logger hijo, p. ej. obtener_logger('historial') -> 'calculadora.historial'."""
    return logging.getLogger(f"{NOMBRE_LOGGER_BASE}.{nombre}")


def obtener_logs_recientes(cantidad=100, niveles=None, ruta=RUTA_LOG) -> list:
    """Lee los registros recientes (modo consulta). Si no existe el archivo devuelve []."""
    if not ruta.exists():
        obtener_logger("logs").warning("archivo de logs aún inexistente | %s", ruta.name)
        return []
    return ultimas_lineas_log(ruta, cantidad, niveles)
