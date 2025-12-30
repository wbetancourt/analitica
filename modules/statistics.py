import pandas as pd

def kpis_generales(df_consumos, df_usuarios):
    total_usuarios = df_usuarios["id_usuario"].nunique()
    consumo_total = df_consumos["consumo_kwh"].sum()
    consumo_promedio = df_consumos["consumo_kwh"].mean()

    return {
        "total_usuarios": total_usuarios,
        "consumo_total": consumo_total,
        "consumo_promedio": consumo_promedio
    }


def consumo_por_tipo(df_consumos, df_usuarios):
    df = df_consumos.merge(
        df_usuarios[["id_usuario", "tipo_usuario"]],
        on="id_usuario"
    )

    return df.groupby("tipo_usuario")["consumo_kwh"].mean().reset_index()
