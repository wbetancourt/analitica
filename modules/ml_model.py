import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def detectar_anomalias(df_consumos):
    """
    Aplica Isolation Forest para detectar consumos anómalos
    """

    # Variables para el modelo
    features = df_consumos[["consumo_kwh", "variacion_pct"]]

    # Escalado
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    # Modelo Isolation Forest
    model = IsolationForest(
        n_estimators=100,
        contamination=0.15,
        random_state=42
    )

    df_consumos = df_consumos.copy()

    # Entrenamiento y predicción
    df_consumos["anomalia"] = model.fit_predict(X_scaled)
    df_consumos["score_anomalia"] = model.decision_function(X_scaled)

    # Convertir a etiqueta clara
    df_consumos["anomalia"] = df_consumos["anomalia"].map({
        1: "Normal",
        -1: "Anómalo"
    })

    return df_consumos
