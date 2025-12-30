import streamlit as st
import plotly.express as px
from modules.ingestion import cargar_datos
from modules.irregularities import (
    resumen_irregularidades,
    irregularidades_por_usuario
)

st.title("🧾 Irregularidades y energía no facturada")

_, _, df_irregularidades, _ = cargar_datos()

if df_irregularidades.empty:
    st.warning("No hay irregularidades registradas")
    st.stop()

# Resumen general
st.subheader("📌 Resumen por tipo de irregularidad")
resumen = resumen_irregularidades(df_irregularidades)
st.dataframe(resumen)

fig = px.bar(
    resumen, 
    x="tipo_irregularidad", 
    y="energia_no_facturada_kwh", 
    title="Impacto energético por tipo de irregularidad",
    labels={"energia_no_facturada_kwh": "kWh no facturados"}
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Ranking usuarios
st.subheader("🚨 Usuarios con mayor energía no facturada")
ranking = irregularidades_por_usuario(df_irregularidades)
ranking = ranking.sort_values(
    by="energia_no_facturada_kwh",
    ascending=False
)

st.dataframe(ranking.head(10))
