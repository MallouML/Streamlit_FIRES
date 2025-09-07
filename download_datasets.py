from download_datasets import DATA_DIR, datasets
import pandas as pd
import os
import streamlit as st

# Téléchargement automatique des datasets
for filename, url in datasets.items():
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        st.write(f"Téléchargement de {filename}...")
        import gdown
        gdown.download(url, filepath, quiet=False)
        st.write(f"{filename} téléchargé !")
    else:
        st.write(f"{filename} existe déjà, skip.")

# Charger les CSV
df_fires = pd.read_csv(os.path.join(DATA_DIR, "fires.csv"))
df_weather = pd.read_csv(os.path.join(DATA_DIR, "US_wildfire_weather_data.csv"))
df_v2 = pd.read_csv(os.path.join(DATA_DIR, "dataset_v2.csv"))

st.write("Datasets chargés !")
