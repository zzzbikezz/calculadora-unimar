"""Página 4: Fundamentos / Ayuda."""
import streamlit as st

from calculadora.materiales import MATERIALES


def mostrar():
    st.title("📘 Fundamentos y ayuda")
    st.header("Parámetros de entrada")
    st.markdown("""
| Dato | Significado | Validación |
|---|---|---|
| Tensión (V) | Voltaje DC de la fuente | número > 0 |
| Rcarga (Ω) | Resistencia del dispositivo (≠ resistencia del cable) | número > 0 |
| Material | Selector fijo; define la resistividad ρ | solo la lista |
| Longitud de ida L (m) | Distancia fuente-carga (el retorno se suma automáticamente) | número > 0 |
| Sección A (mm²) | Área del conductor (no diámetro, radio ni AWG) | número > 0 |
""")
    st.header("Fórmulas (en este orden)")
    st.latex(r"A_{m^2}=A_{mm^2}\times 10^{-6}")
    st.latex(r"L_{total}=2L")
    st.latex(r"R_c=\rho\,\frac{L_{total}}{A_{m^2}}")
    st.latex(r"R_t=R_{carga}+R_c")
    st.latex(r"I=\frac{V}{R_t}")
    st.latex(r"V_c=I\,R_c \qquad P_c=I^2R_c")
    st.header("Resistividades a 20 °C (Ω·m)")
    st.table({"Material": list(MATERIALES), "ρ (Ω·m)": [f"{x:.2e}" for x in MATERIALES.values()]})
    st.header("Ejemplo")
    st.markdown("**V=12 V, Rcarga=10 Ω, cobre, L=5 m, A=2,5 mm²** → "
                "Rc≈0,0672 Ω · Rt≈10,0672 Ω · I≈1,1920 A · Vc≈0,0801 V · Pc≈0,0955 W")
    st.header("Formatos de sección")
    st.markdown("✅ Admitidos: `2.5`, `2,5`, `2.5 mm2`, `2,5 mm²`  \n❌ Rechazados: `2.5 cm2`, `AWG 12`, `dos`, `0`, `-2`, vacío, `nan`, `inf`")
    st.header("Historial vs. Logs")
    st.markdown("- **Historial** (`data/historial.json`): qué cálculos hizo el usuario.\n"
                "- **Logs** (`logs/app.log`): qué eventos técnicos ocurrieron (INFO / WARNING / ERROR).")
    st.header("Supuestos y limitaciones")
    st.warning("Simulación didáctica de un circuito DC ideal a 20 °C. No calcula ampacidad ni corriente máxima "
               "admisible, no considera calentamiento ni resistencia de contactos, y no sirve para dimensionar "
               "instalaciones eléctricas reales.")
