import pandas as pd
from modules.chatbot import detectar_intencion, responder

# ------------------------
# DATOS DE PRUEBA
# ------------------------
df_usuarios = pd.DataFrame({
    "id_usuario": [1, 2, 3],
    "tipo_usuario": ["Residencial", "Comercial", "Industrial"]
})

df_consumos = pd.DataFrame({
    "id_usuario": [1, 2, 3],
    "consumo_kwh": [120, 450, 900],
    "variacion_pct": [-10, -35, -5]
})

df_irregularidades = pd.DataFrame({
    "id_usuario": [2],
    "tipo": ["Manipulación"]
})

df_deudas = pd.DataFrame({
    "id_usuario": [1, 2, 3],
    "deuda_total": [50000, 120000, 30000]
})

# ------------------------
# PRUEBA DEL CHATBOT
# ------------------------
pregunta = "usuarios con mayor caída de consumo"
intencion = detectar_intencion(pregunta)

respuesta = responder(
    intencion,
    df_usuarios,
    df_consumos,
    df_irregularidades,
    df_deudas
)

print(respuesta)
