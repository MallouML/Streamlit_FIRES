import os
import gdown
import pandas as pd
import streamlit as st

DATA_DIR = os.path.join(os.path.dirname(__file__), "Datasets")
os.makedirs(DATA_DIR, exist_ok=True)

datasets = {
    "US_wildfire_weather_data.csv": "1FfGg56InKnFMUcF8WFGQcFjWUMCB7dVY",
    "fires.csv": "1IhF1oK34yVs-gxsh8et8DsNHwOI5FZDc",
    "dataset_v2.csv": "1FXfZQpwLOX-3qoh0d2r1IiapZrr4y7NS"
}

@st.cache_data
def load_data():
    # Télécharger si le fichier n'existe pas
    for filename, file_id in datasets.items():
        filepath = os.path.join(DATA_DIR, filename)
        if not os.path.exists(filepath):
            url = f"https://drive.google.com/uc?id={file_id}"
            gdown.download(url, filepath, quiet=False)
    
    # Charger les CSV
    df1 = pd.read_csv(os.path.join(DATA_DIR, "fires.csv"))
    df2 = pd.read_csv(os.path.join(DATA_DIR, "US_wildfire_weather_data.csv"))
    df3 = pd.read_csv(os.path.join(DATA_DIR, "dataset_v2.csv"))
    return df1, df2, df3
