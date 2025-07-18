import pandas as pd
from datetime import datetime

RACKS = ['R1', 'R2', 'R3', 'R4', 'R5']
FILAS = ['A', 'B', 'C', 'D', 'E', 'F']
COLUMNAS = ['1', '2', '3', '4']

def cargar_datos(path="data/pallets.csv"):
    """
    Carga los datos de stock desde un archivo CSV. Si el archivo no existe, 
    genera un DataFrame con todos los slots vacíos según la estructura definida.

    Args:
        path (str): Ruta del archivo CSV a cargar.

    Retorna:
        pd.DataFrame: DataFrame con los datos de stock.
    """
    try:
        df = pd.read_csv(path)
        df['fecha_vto'] = pd.to_datetime(df['fecha_vto'], errors='coerce')
        df['fecha_produccion'] = pd.to_datetime(df['fecha_produccion'], errors='coerce')
        df['fecha_acomodado'] = pd.to_datetime(df['fecha_acomodado'], errors='coerce')
        return df
    except FileNotFoundError:
        # Crear dataframe base vacío con todos los slots
        data = []
        for rack in RACKS:
            for fila in FILAS:
                for col in COLUMNAS:
                    slot = f"{fila}{col}"
                    data.append({
                        "rack": rack,
                        "slot": slot,
                        "producto": "",
                        "fecha_vto": pd.NaT,
                        "cantidad": 0,
                        "fecha_produccion": pd.NaT,
                        "fecha_acomodado": pd.NaT,
                        "lote": ""
                    })
        return pd.DataFrame(data)

def guardar_datos(df, path="data/pallets.csv"):
    """
    Guarda el DataFrame con los datos de stock en un archivo CSV.

    Args:
        df (pd.DataFrame): DataFrame con los datos a guardar.
        path (str): Ruta del archivo CSV donde guardar los datos.
    """
    df.to_csv(path, index=False)
