# utils.py
import os
import gdown
import pandas as pd

DATA_DIR = "Datasets"
os.makedirs(DATA_DIR, exist_ok=True)

# Dictionnaire des datasets à télécharger
datasets = {
    "US_wildfire_weather_data.csv": "1FfGg56InKnFMUcF8WFGQcFjWUMCB7dVY",
    "fires.csv": "1IhF1oK34yVs-gxsh8et8DsNHwOI5FZDc",
    "dataset_v2.csv": "1FXfZQpwLOX-3qoh0d2r1IiapZrr4y7NS"
}

def download_dataset(filename: str):
    """Télécharge un dataset spécifique depuis Google Drive si absent"""
    if filename not in datasets:
        raise ValueError(f"{filename} n'est pas dans la liste des datasets connus.")
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Téléchargement de {filename}...")
        url = f"https://drive.google.com/uc?id={datasets[filename]}"
        gdown.download(url, filepath, quiet=False)
        print(f"{filename} téléchargé !")
    else:
        print(f"{filename} existe déjà, skip.")
    return filepath

def download_all():
    """Télécharge tous les datasets"""
    for filename in datasets:
        download_dataset(filename)

def load_csv(filename: str, low_memory=True, **kwargs):
    """Charge un CSV depuis le dossier DATA_DIR"""
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        download_dataset(filename)
    return pd.read_csv(filepath, low_memory=low_memory, **kwargs)

def load_data(filename: str, low_memory=True, **kwargs):
    """Alias pour load_csv pour compatibilité avec l'ancien code"""
    return load_csv(filename, low_memory=low_memory, **kwargs)

def load_all(low_memory=True):
    """
    Charge tous les datasets et retourne les DataFrames
    Usage : df1, df2, df3 = load_all()
    """
    df1 = load_data("US_wildfire_weather_data.csv", low_memory=low_memory)
    df2 = load_data("fires.csv", low_memory=low_memory)
    df3 = load_data("dataset_v2.csv", low_memory=low_memory)
    return df1, df2, df3
