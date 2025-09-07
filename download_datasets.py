import os
import gdown

DATA_DIR = "Datasets"
os.makedirs(DATA_DIR, exist_ok=True)

datasets = {
    "US_wildfire_weather_data.csv": "https://drive.google.com/uc?id=ID1",
    "fires.csv": "https://drive.google.com/uc?id=ID2",
    "dataset_v2.csv": "https://drive.google.com/uc?id=ID3"
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
