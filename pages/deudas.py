import streamlit as st
import plotly.express as px
from modules.ingestion import cargar_datos
from modules.recovery import (
    resumen_deudas,
    ranking_deudores,
    deuda_por_meses
)

st.title("💰 Deudas e impacto económico")

_, _, _, df_deudas = cargar_datos()

if df_deudas.empty:
    st.warning("No hay información de deudas")
    st.stop()

# KPIs
resumen = resumen_deudas(df_deudas)

col1, col2, col3 = st.columns(3)
col1.metric("Deuda total", f"${resumen['deuda_total']:,.0f}")
col2.metric("Deuda promedio", f"${resumen['deuda_promedio']:,.0f}")
col3.metric("Usuarios en mora", resumen["usuarios_mora"])

st.divider()

# Ranking
st.subheader("🚨 Top usuarios con mayor deuda")
st.dataframe(ranking_deudores(df_deudas))

st.divider()

# Deuda por meses
st.subheader("📊 Deuda según meses de mora")
df_meses = deuda_por_meses(df_deudas)

fig = px.bar(df_meses, x="meses_mora", y="deuda_total", labels={
    "meses_mora": "Meses de mora",
    "deuda_total": "Deuda total"
})
st.plotly_chart(fig, use_container_width=True)
