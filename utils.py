# utils.py
import os
import pandas as pd

DATA_DIR = "Datasets"

def load_data(filename: str):
    """
    Charge un fichier Parquet depuis le dossier Datasets.
    """
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filepath} est introuvable.")
    return pd.read_parquet(filepath)
