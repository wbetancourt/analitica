import pandas as pd

def detectar_variaciones(df_consumos):
    df = df_consumos.copy()

    # Marca caídas fuertes
    df["caida_fuerte"] = df["variacion_pct"] < -30

    # Cálculo por usuario
    resumen = (
        df.groupby("id_usuario")
        .agg(
            variacion_media=("variacion_pct", "mean"),
            min_variacion=("variacion_pct", "min"),
            meses_criticos=("caida_fuerte", "sum")
        )
        .reset_index()
    )

    return df, resumen


def ranking_sospechosos(resumen, top_n=10):
    return resumen.sort_values(
        by=["meses_criticos", "min_variacion"],
        ascending=[False, True]
    ).head(top_n)
