# streamlit_app.py
import streamlit as st
import os
import gdown
import pandas as pd

# --- Création du dossier pour les datasets ---
DATA_DIR = "Datasets"
os.makedirs(DATA_DIR, exist_ok=True)

# --- Dictionnaire des fichiers à télécharger depuis Google Drive ---
datasets = {
    "fires.csv": "1IhF1oK34yVs-gxsh8et8DsNHwOI5FZDc",
    "US_wildfire_weather_data.csv": "1FfGg56InKnFMUcF8WFGQcFjWUMCB7dVY",
    "dataset_v2.csv": "1FXfZQpwLOX-3qoh0d2r1IiapZrr4y7NS"
}

# --- Fonction pour télécharger les fichiers si nécessaire ---
def download_all():
    for filename, file_id in datasets.items():
        filepath = os.path.join(DATA_DIR, filename)
        if not os.path.exists(filepath):
            st.info(f"Téléchargement de {filename}...")
            url = f"https://drive.google.com/uc?id={file_id}"
            gdown.download(url, filepath, quiet=False)
            st.success(f"{filename} téléchargé !")
        else:
            st.write(f"{filename} existe déjà, skip.")

# --- Charger les fichiers CSV ---
@st.cache_data
def load_data():
    download_all()  # s'assurer que tous les fichiers sont présents
    df1 = pd.read_csv(os.path.join(DATA_DIR, "fires.csv"))
    df2 = pd.read_csv(os.path.join(DATA_DIR, "US_wildfire_weather_data.csv"))
    df = pd.read_csv(os.path.join(DATA_DIR, "dataset_v2.csv"))
    return df1, df2, df

# --- Utilisation des données dans Streamlit ---
df1, df2, df3 = load_data()

st.title("Projet Feux USA")
st.write("Aperçu du dataset `fires.csv`")
st.dataframe(df1.head())

st.write("Aperçu du dataset `US_wildfire_weather_data.csv`")
st.dataframe(df2.head())

st.write("Aperçu du dataset `dataset_v2.csv`")
st.dataframe(df.head())
