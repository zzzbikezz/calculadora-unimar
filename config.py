"""Configuración global: rutas RELATIVAS al proyecto y formatos de logs.

Usar Path(__file__) hace que el programa funcione en cualquier computadora,
sin importar desde qué carpeta se ejecute.
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
DIR_DATA = RAIZ / "data"
DIR_LOGS = RAIZ / "logs"
DIR_REPORTES = RAIZ / "reportes"

RUTA_HISTORIAL = DIR_DATA / "historial.json"
RUTA_LOG = DIR_LOGS / "app.log"

NOMBRE_LOGGER_BASE = "calculadora"
FORMATO_LOG = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"
