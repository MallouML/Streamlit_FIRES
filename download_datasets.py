import os
import gdown

DATA_DIR = "Datasets"
os.makedirs(DATA_DIR, exist_ok=True)

datasets = {
    "US_wildfire_weather_data.csv": "https://drive.google.com/file/d/1FfGg56InKnFMUcF8WFGQcFjWUMCB7dVY/view?usp=drive_link",
    "fires.csv": "https://drive.google.com/file/d/1IhF1oK34yVs-gxsh8et8DsNHwOI5FZDc/view?usp=drive_link",
    "dataset_v2.csv": "https://drive.google.com/file/d/1FXfZQpwLOX-3qoh0d2r1IiapZrr4y7NS/view?usp=drive_link"
}

def download_all():
    for filename, url in datasets.items():
        filepath = os.path.join(DATA_DIR, filename)
        if not os.path.exists(filepath):
            print(f"Téléchargement de {filename}...")
            gdown.download(url, filepath, quiet=False)
            print(f"{filename} téléchargé !")
        else:
            print(f"{filename} existe déjà, skip.")
