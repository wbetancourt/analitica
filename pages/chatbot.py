import streamlit as st
import pandas as pd
import plotly.express as px

from modules.chatbot import detectar_intencion, responder
from modules.ingestion import cargar_datos


st.title("🤖 Chatbot de Consumo Energético")

# ============================
# VALIDAR / CARGAR DATOS
# ============================
if "df_consumos" not in st.session_state:
    df_usuarios, df_consumos, df_irregularidades, df_deudas = cargar_datos()

    st.session_state.df_usuarios = df_usuarios
    st.session_state.df_consumos = df_consumos
    st.session_state.df_irregularidades = df_irregularidades
    st.session_state.df_deudas = df_deudas
else:
    df_usuarios = st.session_state.df_usuarios
    df_consumos = st.session_state.df_consumos
    df_irregularidades = st.session_state.df_irregularidades
    df_deudas = st.session_state.df_deudas


# ============================
# INPUT DEL CHATBOT
# ============================
pregunta = st.text_input("Escribe tu pregunta:")

# ============================
# PROCESAR RESPUESTA
# ============================
if pregunta:

    intencion = detectar_intencion(pregunta)

    respuesta = responder(
        intencion,
        df_usuarios,
        df_consumos,
        df_irregularidades,
        df_deudas
    )

    # ============================
    # RESPUESTAS GRÁFICAS
    # ============================
    if isinstance(respuesta, dict) and respuesta.get("tipo") == "grafico":

        grafico = respuesta.get("grafico")

        if grafico == "scatter_consumo_variacion":
            fig = px.scatter(
                df_consumos,
                x="consumo_kwh",
                y="variacion_pct",
                title="Consumo vs Variación porcentual"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif grafico == "histograma_consumo":
            fig = px.histogram(
                df_consumos,
                x="consumo_kwh",
                nbins=20,
                title="Distribución del consumo energético"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif grafico == "ranking_sospechosos":
            ranking = (
                df_consumos[df_consumos["variacion_pct"] < -30]
                .sort_values("variacion_pct")
                .head(10)
            )

            fig = px.bar(
                ranking,
                x="variacion_pct",
                y=ranking["id_usuario"].astype(str),
                orientation="h",
                title="Ranking de usuarios sospechosos"
            )
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("📊 Gráfico no reconocido por el sistema")

    # ============================
    # RESPUESTAS TABULARES
    # ============================
    elif isinstance(respuesta, pd.DataFrame):
        st.dataframe(respuesta, use_container_width=True)

    # ============================
    # RESPUESTAS TEXTO
    # ============================
    else:
        st.write(respuesta)
