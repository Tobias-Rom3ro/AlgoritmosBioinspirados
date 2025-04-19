import os
import glob
import pandas as pd

def find_excel():
    """Busca automáticamente un archivo .xlsx."""
    cwd = os.path.dirname(os.path.abspath(__file__))
    archivos = glob.glob(os.path.join(cwd, '*.xlsx'))
    if archivos:
        return archivos[0]
    raise FileNotFoundError("No se encontró ningún archivo .xlsx en la carpeta actual.")

def load_data(file_path, max_weight=None):
    """
    Carga datos del Excel encontrado.
    Devuelve un diccionario (los datos del excel).
    """
    try:
        df = pd.read_excel(file_path)
        print("Columnas encontradas:", df.columns.tolist())

        # Detecta columnas o solicita nombres
        weight_col = ('Peso_kg' if 'Peso_kg' in df.columns else
                      'Peso (kg)' if 'Peso (kg)' in df.columns else
                      input("Columna de pesos: "))
        value_col = ('Valor' if 'Valor' in df.columns else
                     'Valor ($)' if 'Valor ($)' in df.columns else
                     input("Columna de valores: "))
        qty_col = ('Cantidad' if 'Cantidad' in df.columns else
                   input("Columna de cantidades: "))

        weights = df[weight_col].astype(float).tolist()
        values = df[value_col].astype(float).tolist()
        quantities = df[qty_col].astype(int).tolist()
        n_items = len(weights)

        # Capacidad máxima de la mochila
        if max_weight is None:
            filename = os.path.basename(file_path)
            if "capacidad" in filename.lower():
                try:
                    parts = filename.lower().split("capacidad_maxima_")
                    w_str = parts[1].split("kg")[0]
                    max_weight = float(w_str)
                    print(f"Capacidad extraída: {max_weight} kg")
                except:
                    max_weight = float(input("Ingrese la capacidad máxima (kg): "))
            else:
                max_weight = float(input("Ingrese la capacidad máxima (kg): "))

        print(f"Datos cargados: {n_items} objetos, capacidad {max_weight} kg")

        return {
            "weights": weights,
            "values": values,
            "quantities": quantities,
            "max_weight": max_weight,
            "n_items": n_items
        }

    except Exception as e:
        print(f"Error al cargar datos: {e}")
        return None