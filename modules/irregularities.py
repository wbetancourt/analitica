import pandas as pd

def resumen_irregularidades(df_irregularidades):
    return (
        df_irregularidades
        .groupby("tipo_irregularidad")
        .agg(
            casos=("id_usuario", "count"),
            energia_no_facturada_kwh=("energia_no_facturada_kwh", "sum")
        )
        .reset_index()
    )


def irregularidades_por_usuario(df_irregularidades):
    return (
        df_irregularidades
        .groupby("id_usuario")
        .agg(
            casos=("tipo_irregularidad", "count"),
            energia_no_facturada_kwh=("energia_no_facturada_kwh", "sum")
        )
        .reset_index()
    )
