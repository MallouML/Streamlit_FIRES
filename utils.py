# utils.py
import os
import pandas as pd

DATA_DIR = "Datasets"

def load_data(filename: str):
    """
    Charge un fichier Parquet depuis le dossier Datasets
    ou une URL externe.
    """
    # Si c'est une URL (http/https)
    if filename.startswith("http"):
        return pd.read_parquet(filename)

    # Sinon, chemin local
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filepath} est introuvable dans {DATA_DIR}/")

    return pd.read_parquet(filepath)
