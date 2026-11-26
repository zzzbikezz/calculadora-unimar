"""Excepciones propias del proyecto (se usan con raise / try-except)."""


class ErrorDeValidacion(ValueError):
    """Un dato de entrada no cumple las reglas. Lleva el campo afectado."""

    def __init__(self, campo: str, mensaje: str):
        self.campo = campo
        self.mensaje = mensaje
        super().__init__(f"{campo}: {mensaje}")


class HistorialError(Exception):
    """Fallo al leer o escribir data/historial.json."""


class ReporteError(Exception):
    """Fallo al generar o exportar un reporte CSV."""
