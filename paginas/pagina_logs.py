"""Página 3: Logs técnicos (solo consulta). Lee logs/app.log con un generador."""
import streamlit as st

from servicios.logs import obtener_logs_recientes


def mostrar():
    st.title("🧾 Logs técnicos")
    st.caption("Eventos del programa (inicio, validaciones, lecturas/escrituras, exportaciones, errores). "
               "No es el historial de cálculos.")
    c1, c2 = st.columns([1, 2])
    cantidad = c1.slider("Cantidad de líneas recientes", 10, 500, 50, step=10)
    niveles = c2.multiselect("Niveles", ["INFO", "WARNING", "ERROR"], default=["INFO", "WARNING", "ERROR"])
    lineas = obtener_logs_recientes(cantidad, niveles)
    if not lineas:
        st.info("No hay líneas de log para mostrar.")
        return
    m1, m2, m3 = st.columns(3)
    for caja, nivel in zip((m1, m2, m3), ("INFO", "WARNING", "ERROR")):
        caja.metric(nivel, sum(1 for l in lineas if f"| {nivel} |" in l))
    st.code("\n".join(lineas), language="text")  # solo lectura
