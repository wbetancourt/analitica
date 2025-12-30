import streamlit as st
import plotly.express as px
from modules.ingestion import cargar_datos
from modules.descriptive_stats import estadisticas_consumo
import pandas as pd 
st.title("📊 Estadística descriptiva del consumo")

df_usuarios, df_consumos, _, _ = cargar_datos()

# Sidebar – filtros
st.sidebar.header("Filtros")

tipo_usuario = st.sidebar.multiselect(
    "Tipo de usuario",
    options=df_usuarios["tipo_usuario"].unique(),
    default=df_usuarios["tipo_usuario"].unique()
)

estratos = st.sidebar.multiselect(
    "Estrato (solo residencial)",
    options=sorted(df_usuarios["estrato"].dropna().unique())
)

fecha_min = df_consumos["fecha"].min()
fecha_max = df_consumos["fecha"].max()

rango_fechas = st.sidebar.date_input(
    "Rango de fechas",
    [fecha_min, fecha_max]
)

# Filtro usuarios
df_filtrado = df_consumos.merge(
    df_usuarios,
    on="id_usuario"
)

df_filtrado = df_filtrado[
    df_filtrado["tipo_usuario"].isin(tipo_usuario)
]

if estratos:
    df_filtrado = df_filtrado[
        df_filtrado["estrato"].isin(estratos)
    ]

df_filtrado = df_filtrado[
    (df_filtrado["fecha"] >= pd.to_datetime(rango_fechas[0])) &
    (df_filtrado["fecha"] <= pd.to_datetime(rango_fechas[1]))
]

# Estadísticas
stats = estadisticas_consumo(df_filtrado)

st.subheader("📌 Métricas estadísticas")
cols = st.columns(4)

for i, (k, v) in enumerate(stats.items()):
    cols[i % 4].metric(k, f"{v:,.2f}")

st.divider()

# Histograma
st.subheader("📈 Distribución del consumo (kWh)")
fig = px.histogram(
    df_filtrado, 
    x="consumo_kwh", 
    nbins=30, 
    labels={"consumo_kwh": "Consumo kWh"}
)
fig.update_layout(yaxis_title="Frecuencia")
st.plotly_chart(fig, use_container_width=True)
