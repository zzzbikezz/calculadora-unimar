"""Página 1: Calculadora (interfaz). Solo muestra y recoge datos; la lógica vive en calculadora/."""
import streamlit as st

from calculadora.calculos import calcular_circuito, formatear_resultados
from calculadora.excepciones import ErrorDeValidacion, HistorialError
from calculadora.materiales import listar_materiales
from calculadora.validaciones import validar_entradas
from servicios.historial import guardar_calculo
from servicios.logs import obtener_logger

log = obtener_logger("calcular")
CAMPOS = ("in_tension", "in_carga", "in_longitud", "in_seccion")
EJEMPLO = {"in_tension": "12", "in_carga": "10", "in_material": "cobre",
           "in_longitud": "5", "in_seccion": "2,5 mm²"}


def _limpiar():
    for clave in CAMPOS:
        st.session_state[clave] = ""
    st.session_state["in_material"] = listar_materiales()[0]
    st.session_state.pop("ultimo_calculo", None)


def _cargar_ejemplo():
    for clave, valor in EJEMPLO.items():
        st.session_state[clave] = valor


def mostrar():
    st.title("⚡ Calculadora de corriente y resistencia (DC)")
    st.caption("Circuito DC resistivo en serie: fuente → cable de ida → carga → cable de retorno.")
    for clave in CAMPOS:
        st.session_state.setdefault(clave, "")
    st.session_state.setdefault("in_material", listar_materiales()[0])

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Tensión (V)", key="in_tension", placeholder="Ej: 12")
        st.text_input("Resistencia de carga Rcarga (Ω)", key="in_carga", placeholder="Ej: 10")
        st.selectbox("Material del conductor", listar_materiales(), key="in_material")
    with col2:
        st.text_input("Longitud de ida L (m)", key="in_longitud", placeholder="Ej: 5  (el retorno se duplica solo)")
        st.text_input("Sección transversal A (mm²)", key="in_seccion", placeholder="Ej: 2,5  ó  2.5 mm2")

    b1, b2, b3, _ = st.columns([1, 1, 1, 3])
    calcular = b1.button("Calcular", type="primary")
    b2.button("Limpiar", on_click=_limpiar)
    b3.button("Cargar ejemplo", on_click=_cargar_ejemplo)

    if calcular:
        try:
            datos = validar_entradas(st.session_state["in_tension"], st.session_state["in_carga"],
                                     st.session_state["in_material"], st.session_state["in_longitud"],
                                     st.session_state["in_seccion"])
            resultados = calcular_circuito(**datos)
            try:
                registro = guardar_calculo(datos, resultados)
                log.info("cálculo completado | id=%s", registro["id"])
                st.session_state["ultimo_calculo"] = registro
            except HistorialError as error:
                st.warning(f"El cálculo se hizo, pero no se pudo guardar en el historial: {error}")
                st.session_state["ultimo_calculo"] = {"id": "—", "entradas": datos, "resultados": resultados}
        except ErrorDeValidacion as error:
            st.session_state.pop("ultimo_calculo", None)
            st.error(f"⚠️ Revise **{error.campo}**: {error.mensaje}")
        except Exception as error:  # último recurso: la app nunca se cierra
            log.error("excepción inesperada en la calculadora | %s: %s", type(error).__name__, error)
            st.error("Ocurrió un error inesperado. Revise la pestaña Logs.")

    ultimo = st.session_state.get("ultimo_calculo")
    if ultimo:
        st.success(f"Cálculo guardado en el historial con id **{ultimo['id']}**.")
        columnas = st.columns(5)
        for columna, (simbolo, valor, unidad, ayuda) in zip(columnas, formatear_resultados(ultimo["resultados"])):
            columna.metric(f"{simbolo} ({unidad})", f"{valor} {unidad}", help=ayuda)
        st.caption("Simulación didáctica a 20 °C. No calcula ampacidad ni sirve para dimensionar instalaciones reales.")
