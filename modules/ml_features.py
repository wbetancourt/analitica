import pandas as pd

def construir_dataset_ml(
    df_usuarios,
    df_consumos,
    df_irregularidades,
    df_deudas
):
    # Consumo por usuario
    cons = (
        df_consumos.groupby("id_usuario")
        .agg(
            consumo_promedio=("consumo_kwh", "mean"),
            desviacion_consumo=("consumo_kwh", "std"),
            variacion_media=("variacion_pct", "mean"),
            min_variacion=("variacion_pct", "min"),
            meses_criticos=("variacion_pct", lambda x: (x < -30).sum())
        )
        .reset_index()
    )

    # Irregularidades
    irr = (
        df_irregularidades.groupby("id_usuario")
        .agg(
            total_irregularidades=("tipo_irregularidad", "count"),
            energia_no_facturada_kwh=("energia_no_facturada_kwh", "sum")
        )
        .reset_index()
    )

    # Deudas
    deuda = df_deudas.copy()

    # Merge
    df = cons.merge(irr, on="id_usuario", how="left") \
             .merge(deuda, on="id_usuario", how="left") \
             .merge(df_usuarios[["id_usuario", "tipo_usuario"]], on="id_usuario")

    df.fillna(0, inplace=True)

    # Target
    df["sospechoso"] = (
        (df["meses_criticos"] >= 2) |
        (df["total_irregularidades"] > 0)
    ).astype(int)

    # One-hot
    df = pd.get_dummies(df, columns=["tipo_usuario"], drop_first=True)

    return df
