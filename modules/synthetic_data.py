import numpy as np
import pandas as pd

def generar_usuarios(n=500):
    tipos = ["Residencial", "Comercial", "Industrial"]
    barrios = ["Centro", "Norte", "Sur", "Oriente", "Occidente"]

    data = []
    for i in range(n):
        tipo = np.random.choice(tipos, p=[0.7, 0.2, 0.1])
        estrato = np.random.randint(1, 7) if tipo == "Residencial" else None

        data.append([
            i,
            tipo,
            estrato,
            np.random.choice(barrios),
            "Activo"
        ])

    return pd.DataFrame(
        data,
        columns=["id_usuario", "tipo_usuario", "estrato", "barrio", "estado"]
    )


def generar_consumos(df_usuarios, meses=24):
    registros = []
    fechas = pd.date_range(end=pd.Timestamp.today(), periods=meses, freq="M")

    for _, u in df_usuarios.iterrows():
        if u.tipo_usuario == "Residencial":
            base = 120 + (u.estrato or 3) * 30
            ruido = 0.25
        elif u.tipo_usuario == "Comercial":
            base = 900
            ruido = 0.2
        else:
            base = 3000
            ruido = 0.1

        for f in fechas:
            esperado = np.random.normal(base, base * 0.05)
            real = np.random.normal(esperado, esperado * ruido)

            variacion = ((real - esperado) / esperado) * 100

            registros.append([
                u.id_usuario,
                f,
                max(real, 20),
                esperado,
                variacion
            ])

    return pd.DataFrame(
        registros,
        columns=[
            "id_usuario",
            "fecha",
            "consumo_kwh",
            "consumo_esperado_kwh",
            "variacion_pct"
        ]
    )


def generar_irregularidades(df_consumos):
    sospechosos = df_consumos[df_consumos["variacion_pct"] < -30]
    data = []

    for _, r in sospechosos.sample(frac=0.15).iterrows():
        data.append([
            r.id_usuario,
            r.fecha,
            np.random.choice([
                "Manipulación de medidor",
                "Bypass",
                "Conexión directa"
            ]),
            abs(r.variacion_pct) * 20
        ])

    return pd.DataFrame(
        data,
        columns=[
            "id_usuario",
            "fecha_acta",
            "tipo_irregularidad",
            "energia_no_facturada_kwh"
        ]
    )


def generar_deudas(df_irregularidades):
    data = []

    for uid in df_irregularidades["id_usuario"].unique():
        data.append([
            uid,
            np.random.randint(500_000, 15_000_000),
            np.random.randint(3, 24)
        ])

    return pd.DataFrame(
        data,
        columns=["id_usuario", "deuda_total", "meses_mora"]
    )
