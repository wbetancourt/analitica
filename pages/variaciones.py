import streamlit as st
import plotly.express as px
from modules.ingestion import cargar_datos
from modules.variation import detectar_variaciones, ranking_sospechosos

st.title("⚠️ Variaciones y detección de anomalías")

df_usuarios, df_consumos, _, _ = cargar_datos()

# Filtros
st.sidebar.header("Filtros")

tipo_usuario = st.sidebar.multiselect(
    "Tipo de usuario",
    options=df_usuarios["tipo_usuario"].unique(),
    default=df_usuarios["tipo_usuario"].unique()
)

df = df_consumos.merge(
    df_usuarios[["id_usuario", "tipo_usuario"]],
    on="id_usuario"
)

df = df[df["tipo_usuario"].isin(tipo_usuario)]

# Detección
df_detalle, resumen = detectar_variaciones(df)
ranking = ranking_sospechosos(resumen)

# Ranking
st.subheader("🚨 Top usuarios con mayor caída de consumo")
st.dataframe(ranking)

st.divider()

# Gráfica de un usuario seleccionado
usuario_sel = st.selectbox(
    "Selecciona un usuario para ver su comportamiento",
    ranking["id_usuario"]
)

df_user = df_detalle[df_detalle["id_usuario"] == usuario_sel]

fig = px.line(
    df_user, 
    x="fecha", 
    y="consumo_kwh", 
    title=f"Consumo usuario {usuario_sel}", 
    markers=True,
    labels={"consumo_kwh": "kWh"}
)
st.plotly_chart(fig, use_container_width=True)
