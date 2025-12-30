# modules/chatbot.py
from modules.ml_model import detectar_anomalias


def detectar_intencion(texto):
    texto = texto.lower()

    # ============================
    # GRÁFICOS
    # ============================
    if "distribución" in texto or "histograma" in texto:
        return "histograma_consumo"

    if "scatter" in texto or ("consumo" in texto and "variación" in texto):
        return "scatter_consumo_variacion"

    if "mayor caída" in texto or "usuarios sospechosos" in texto:
        return "ranking_sospechosos"

    # ============================
    # ESTADÍSTICAS
    # ============================
    if "promedio" in texto and "consumo" in texto:
        return "consumo_promedio"

    if "comparar" in texto or "vs" in texto:
        return "comparacion_tipos"

    if "irregularidad" in texto:
        return "irregularidades"

    if "no facturada" in texto or "energía" in texto:
        return "energia_no_facturada"

    if "deuda" in texto:
        return "deuda"

    # ============================
    # MACHINE LEARNING
    # ============================
    if "anómalo" in texto or "anomalia" in texto:
        return "usuarios_anomalos"

    if "modelo" in texto or "machine learning" in texto or "ml" in texto:
        return "explicacion_ml"

    if "ayuda" in texto:
        return "ayuda"

    return "desconocida"


def responder(
    intencion,
    df_usuarios,
    df_consumos,
    df_irregularidades,
    df_deudas
):
    # ============================
    # RESPUESTAS ESTADÍSTICAS
    # ============================
    if intencion == "consumo_promedio":
        prom = df_consumos["consumo_kwh"].mean()
        return f"📊 El consumo promedio general es {prom:,.2f} kWh."

    if intencion == "comparacion_tipos":
        df = df_consumos.merge(
            df_usuarios[["id_usuario", "tipo_usuario"]],
            on="id_usuario"
        )
        resumen = df.groupby("tipo_usuario")["consumo_kwh"].mean()
        return resumen.reset_index()

    if intencion == "irregularidades":
        total = len(df_irregularidades)
        return f"🚨 Se registran {total} irregularidades."

    if intencion == "energia_no_facturada":
        total = df_irregularidades["energia_no_facturada_kwh"].sum()
        return f"⚡ La energía no facturada estimada es {total:,.0f} kWh."

    if intencion == "deuda":
        return (
            df_deudas.sort_values(by="deuda_total", ascending=False)
            .head(5)
        )

    # ============================
    # RESPUESTAS CON MACHINE LEARNING
    # ============================
    if intencion == "usuarios_anomalos":
        df_ml = detectar_anomalias(df_consumos)
        total = (df_ml["anomalia"] == "Anómalo").sum()

        return (
            f"🤖 El modelo detectó {total} usuarios con comportamiento anómalo. "
            "Puedes revisar los gráficos en la sección de ML."
        )

    if intencion == "explicacion_ml":
        return (
            "El sistema utiliza Isolation Forest, un algoritmo de "
            "Machine Learning no supervisado, para identificar "
            "patrones de consumo atípicos usando consumo y variación."
        )

    # ============================
    # RESPUESTAS CON GRÁFICOS
    # ============================
    if intencion == "scatter_consumo_variacion":
        return {"tipo": "grafico", "grafico": "scatter_consumo_variacion"}

    if intencion == "histograma_consumo":
        return {"tipo": "grafico", "grafico": "histograma_consumo"}

    if intencion == "ranking_sospechosos":
        return {"tipo": "grafico", "grafico": "ranking_sospechosos"}

    # ============================
    # AYUDA
    # ============================
    if intencion == "ayuda":
        return (
            "Puedes preguntar cosas como:\n"
            "- Distribución del consumo\n"
            "- Usuarios con mayor caída de consumo\n"
            "- Consumo promedio\n"
            "- Usuarios anómalos\n"
            "- Explicación del modelo ML\n"
            "- Ranking de deudas"
        )

    return "❓ No entendí la pregunta. Escribe 'ayuda' para ver ejemplos."
