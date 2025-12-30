import pandas as pd

DATA_PATH = "data/synthetic/"

def cargar_datos():
    usuarios = pd.read_csv(DATA_PATH + "usuarios.csv")
    consumos = pd.read_csv(DATA_PATH + "consumos.csv", parse_dates=["fecha"])
    irregularidades = pd.read_csv(DATA_PATH + "irregularidades.csv", parse_dates=["fecha_acta"])
    deudas = pd.read_csv(DATA_PATH + "deudas.csv")

    return usuarios, consumos, irregularidades, deudas
