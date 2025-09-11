import os
import gdown

DATA_DIR = "Datasets"
os.makedirs(DATA_DIR, exist_ok=True)

datasets = {
    "US_wildfire_weather_data.cvs": "1FfGg56InKnFMUcF8WFGQcFjWUMCB7dVY",
    "fires.csv": "1IhF1oK34yVs-gxsh8et8DsNHwOI5FZDc",
    "dataset_v2.csv": "1FXfZQpwLOX-3qoh0d2r1IiapZrr4y7NS"
}

def download_all():
    for filename, file_id in datasets.items():
        filepath = os.path.join(DATA_DIR, filename)
        if not os.path.exists(filepath):
            print(f"Téléchargement de {filename}...")
            url = f"https://drive.google.com/uc?id={file_id}"
            gdown.download(url, filepath, quiet=False)
            print(f"{filename} téléchargé !")
        else:
            print(f"{filename} existe déjà, skip.")

if __name__ == "__main__":
    download_all()
