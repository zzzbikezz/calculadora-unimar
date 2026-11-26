"""Decorador propio: registra en logs/app.log el nombre y la duración de una operación."""
import functools
import logging
import time

from calculadora.excepciones import ErrorDeValidacion


def registrar_operacion(funcion):
    """Decorador. INFO si termina bien, WARNING si el dato fue inválido, ERROR si falla."""
    modulo = funcion.__module__.split(".")[-1]
    logger = logging.getLogger(f"calculadora.{modulo}.{funcion.__name__}")

    @functools.wraps(funcion)
    def envoltura(*args, **kwargs):
        inicio = time.perf_counter()
        try:
            resultado = funcion(*args, **kwargs)
        except ErrorDeValidacion as error:
            ms = (time.perf_counter() - inicio) * 1000
            logger.warning("operación rechazada por validación | %s | %.3f ms", error, ms)
            raise
        except Exception as error:
            ms = (time.perf_counter() - inicio) * 1000
            logger.error("operación falló | %s: %s | %.3f ms", type(error).__name__, error, ms)
            raise
        ms = (time.perf_counter() - inicio) * 1000
        logger.info("operación completada | duración=%.3f ms", ms)
        return resultado

    return envoltura
