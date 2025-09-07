import os
import requests

DATA_DIR = "Datasets"

# Crée le dossier si nécessaire
os.makedirs(DATA_DIR, exist_ok=True)

datasets = {
    "US_wildfire_weather_data.csv": "https://drive.google.com/uc?export=download&id=ID1",
    "fires.csv": "https://drive.google.com/file/d/1IhF1oK34yVs-gxsh8et8DsNHwOI5FZDc/view?usp=drive_link",
    "dataset_v2.csv": "https://drive.google.com/file/d/1FfGg56InKnFMUcF8WFGQcFjWUMCB7dVY/view?usp=drive_link"
}

for filename, url in datasets.items():
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Téléchargement de {filename}...")
        r = requests.get(url)
        with open(filepath, "wb") as f:
            f.write(r.content)
        print(f"{filename} téléchargé !")
    else:
        print(f"{filename} existe déjà, skip.")
