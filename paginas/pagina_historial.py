"""Página 2: Historial de cálculos (consulta y filtros por fecha o material)."""
from datetime import date

import pandas as pd
import streamlit as st

from calculadora.excepciones import HistorialError
from calculadora.materiales import listar_materiales
from servicios.historial import cargar_historial, filtrar_historial
from servicios.reportes import ENCABEZADOS, registro_a_fila


def mostrar():
    st.title("📜 Historial de cálculos")
    try:
        registros = cargar_historial()
    except HistorialError as error:
        st.error(str(error))
        return
    if not registros:
        st.info("Aún no hay cálculos. Realice uno en la pestaña Calculadora.")
        return

    c1, c2 = st.columns(2)
    material = c1.selectbox("Filtrar por material", ["Todos"] + listar_materiales())
    usar_fecha = c2.checkbox("Filtrar por fecha")
    desde = hasta = None
    if usar_fecha:
        rango = c2.date_input("Rango de fechas", value=(date.today(), date.today()))
        if isinstance(rango, (tuple, list)) and len(rango) == 2:
            desde, hasta = rango
        else:
            st.caption("Seleccione fecha inicial y final.")

    filtrados = filtrar_historial(registros, None if material == "Todos" else material, desde, hasta)
    st.write(f"Mostrando **{len(filtrados)}** de {len(registros)} registros.")
    if filtrados:
        tabla = pd.DataFrame([registro_a_fila(r) for r in reversed(filtrados)], columns=ENCABEZADOS)
        st.dataframe(tabla, hide_index=True)
    else:
        st.warning("Ningún registro coincide con el filtro.")
