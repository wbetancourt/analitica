import streamlit as st
import pandas as pd
import plotly.express as px
from modules.ml_model import detectar_anomalias


# ============================
# CONFIGURACIÓN DE PÁGINA
# ============================
st.set_page_config(
    page_title="Análisis Exploratorio - ML",
    layout="wide"
)

st.title("🧠 Análisis Exploratorio previo a Machine Learning")
st.write(
    "Análisis visual para identificar patrones, comportamientos atípicos "
    "y justificar el uso de modelos de Machine Learning."
)

# ============================
# CARGA DE DATOS
# ============================
df_consumos = st.session_state.df_consumos
df_usuarios = st.session_state.df_usuarios

# ============================
# 1️⃣ HISTOGRAMA DE CONSUMO
# ============================
st.subheader("1️⃣ Distribución del consumo energético")

fig_hist = px.histogram(
    df_consumos,
    x="consumo_kwh",
    nbins=10,
    title="Distribución del consumo energético",
    labels={"consumo_kwh": "Consumo (kWh)"}
)

st.plotly_chart(fig_hist, use_container_width=True)

st.caption(
    "La mayoría de usuarios se concentra en rangos normales, "
    "mientras que los extremos representan posibles anomalías."
)

st.divider()

# ============================
# 4️⃣ SCATTER: CONSUMO VS VARIACIÓN
# ============================
st.subheader("2️⃣ Relación entre consumo y variación porcentual")

fig_scatter = px.scatter(
    df_consumos,
    x="consumo_kwh",
    y="variacion_pct",
    title="Consumo vs Variación porcentual",
    labels={
        "consumo_kwh": "Consumo (kWh)",
        "variacion_pct": "Variación (%)"
    }
)

# Línea de umbral (-30%)
fig_scatter.add_hline(
    y=-30,
    line_dash="dash",
    annotation_text="Umbral de alerta"
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.caption(
    "Usuarios con alto consumo y variaciones negativas pronunciadas "
    "son candidatos prioritarios para análisis avanzado."
)

st.divider()

# ============================
# 6️⃣ RANKING DE USUARIOS SOSPECHOSOS
# ============================
st.subheader("3️⃣ Ranking de usuarios con mayor caída de consumo")

ranking = (
    df_consumos[df_consumos["variacion_pct"] < -30]
    .sort_values("variacion_pct")
    .head(10)
)

fig_rank = px.bar(
    ranking,
    x="variacion_pct",
    y=ranking["id_usuario"].astype(str),
    orientation="h",
    title="Top 10 usuarios con mayor caída de consumo",
    labels={
        "variacion_pct": "Variación (%)",
        "y": "ID Usuario"
    }
)

st.plotly_chart(fig_rank, use_container_width=True)

st.caption(
    "Este ranking define el conjunto objetivo para la aplicación "
    "de modelos de detección de anomalías."
)
st.divider()
st.header("🤖 Detección de anomalías con Machine Learning")

df_ml = detectar_anomalias(df_consumos)

# Métricas
col1, col2 = st.columns(2)
col1.metric(
    "Usuarios analizados",
    len(df_ml)
)
col2.metric(
    "Usuarios anómalos",
    (df_ml["anomalia"] == "Anómalo").sum()
)

# Scatter ML
fig_ml = px.scatter(
    df_ml,
    x="consumo_kwh",
    y="variacion_pct",
    color="anomalia",
    title="Detección de anomalías con Isolation Forest",
    labels={
        "consumo_kwh": "Consumo (kWh)",
        "variacion_pct": "Variación (%)"
    }
)

st.plotly_chart(fig_ml, use_container_width=True)

# Tabla de anomalías
st.subheader("📋 Usuarios detectados como anómalos")

st.dataframe(
    df_ml[df_ml["anomalia"] == "Anómalo"]
    .sort_values("score_anomalia")
    .head(10),
    use_container_width=True
)
