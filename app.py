# app.py

import streamlit as st
from modules.ingestion import cargar_datos
from modules.statistics import kpis_generales, consumo_por_tipo
import plotly.express as px

st.set_page_config(
    page_title="Energy Analytics",
    layout="wide"
)

st.title("⚡ Plataforma Analítica de Consumo Energético")

# 🔹 Cargar datos UNA VEZ
df_usuarios, df_consumos, df_irregularidades, df_deudas = cargar_datos()

# 🔹 Guardarlos en session_state para que el chatbot los use
st.session_state.df_usuarios = df_usuarios
st.session_state.df_consumos = df_consumos
st.session_state.df_irregularidades = df_irregularidades
st.session_state.df_deudas = df_deudas

# KPIs
kpis = kpis_generales(df_consumos, df_usuarios)

col1, col2, col3 = st.columns(3)
col1.metric("Usuarios", kpis["total_usuarios"])
col2.metric("Consumo total (kWh)", f"{kpis['consumo_total']:,.0f}")
col3.metric("Consumo promedio (kWh)", f"{kpis['consumo_promedio']:,.1f}")

st.divider()

# Consumo por tipo
st.subheader("📊 Consumo promedio por tipo de usuario")
df_tipo = consumo_por_tipo(df_consumos, df_usuarios)

fig = px.bar(df_tipo, x="tipo_usuario", y="consumo_kwh")
fig.update_layout(yaxis_title="kWh promedio")
st.plotly_chart(fig, use_container_width=True)
