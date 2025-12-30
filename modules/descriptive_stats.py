import pandas as pd
import numpy as np

def estadisticas_consumo(df):
    return {
        "Media": df["consumo_kwh"].mean(),
        "Mediana": df["consumo_kwh"].median(),
        "Varianza": df["consumo_kwh"].var(),
        "Desv. estándar": df["consumo_kwh"].std(),
        "Mínimo": df["consumo_kwh"].min(),
        "Máximo": df["consumo_kwh"].max(),
        "Percentil 25": np.percentile(df["consumo_kwh"], 25),
        "Percentil 75": np.percentile(df["consumo_kwh"], 75),
    }
