import pandas as pd

def resumen_deudas(df_deudas):
    return {
        "deuda_total": df_deudas["deuda_total"].sum(),
        "deuda_promedio": df_deudas["deuda_total"].mean(),
        "usuarios_mora": df_deudas["id_usuario"].nunique()
    }


def ranking_deudores(df_deudas, top_n=10):
    return (
        df_deudas
        .sort_values(by="deuda_total", ascending=False)
        .head(top_n)
    )


def deuda_por_meses(df_deudas):
    return (
        df_deudas
        .groupby("meses_mora")
        .agg(deuda_total=("deuda_total", "sum"))
        .reset_index()
    )
