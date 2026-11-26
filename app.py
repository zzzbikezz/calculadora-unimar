"""Punto de entrada. Ejecutar con:  streamlit run app.py"""
import streamlit as st

from paginas import (pagina_ayuda, pagina_calculadora, pagina_historial,
                     pagina_logs, pagina_reportes)
from servicios.historial import inicializar_historial
from servicios.logs import configurar_logger, obtener_logger

st.set_page_config(page_title="Calculadora DC · UNIMAR", page_icon="⚡", layout="wide")

configurar_logger()
if "inicio_registrado" not in st.session_state:  # registrar el inicio una vez por sesión
    obtener_logger("app").info("aplicación iniciada")
    st.session_state["inicio_registrado"] = True
inicializar_historial()

PAGINAS = {
    "⚡ Calculadora": pagina_calculadora.mostrar,
    "📜 Historial": pagina_historial.mostrar,
    "🧾 Logs": pagina_logs.mostrar,
    "📘 Fundamentos / Ayuda": pagina_ayuda.mostrar,
    "📤 Reportes": pagina_reportes.mostrar,
}

st.sidebar.title("Calculadora DC")
st.sidebar.caption("Universidad de Margarita · Programación I")
seleccion = st.sidebar.radio("Navegación", list(PAGINAS))
PAGINAS[seleccion]()
