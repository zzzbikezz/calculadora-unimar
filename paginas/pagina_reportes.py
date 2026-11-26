"""Página 5: Reportes CSV (exporta todo el historial o los cálculos seleccionados)."""
import streamlit as st

from calculadora.excepciones import HistorialError, ReporteError
from servicios.historial import cargar_historial
from servicios.reportes import csv_en_bytes, exportar_csv


def mostrar():
    st.title("📤 Reportes CSV")
    try:
        registros = cargar_historial()
    except HistorialError as error:
        st.error(str(error))
        return
    if not registros:
        st.info("No hay cálculos para exportar todavía.")
        return

    ids = [r["id"] for r in registros]
    elegidos = st.multiselect("Cálculos a exportar (vacío = todos)", ids)
    seleccion = [r for r in registros if not elegidos or r["id"] in elegidos]
    st.write(f"Se exportarán **{len(seleccion)}** registros con encabezados y unidades.")

    c1, c2 = st.columns(2)
    if c1.button("Guardar CSV en la carpeta reportes/", type="primary"):
        try:
            ruta = exportar_csv(seleccion)
            st.success(f"Reporte guardado: reportes/{ruta.name}")
        except ReporteError as error:
            st.error(str(error))
    try:
        c2.download_button("⬇️ Descargar CSV", data=csv_en_bytes(seleccion),
                           file_name="reporte_calculos.csv", mime="text/csv")
    except ReporteError as error:
        c2.warning(str(error))
