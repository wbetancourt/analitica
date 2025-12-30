from synthetic_data import *

usuarios = generar_usuarios(800)
consumos = generar_consumos(usuarios)
irregularidades = generar_irregularidades(consumos)
deudas = generar_deudas(irregularidades)

usuarios.to_csv("data/synthetic/usuarios.csv", index=False)
consumos.to_csv("data/synthetic/consumos.csv", index=False)
irregularidades.to_csv("data/synthetic/irregularidades.csv", index=False)
deudas.to_csv("data/synthetic/deudas.csv", index=False)

print("✔ Datos sintéticos generados")
