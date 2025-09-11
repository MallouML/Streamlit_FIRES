import streamlit as st
import pandas as pd
from PIL import Image


#/Users/mallou/Documents/Projet\ Data/Feux_USA/.conda/bin/streamlit run "/Users/mallou/Documents/Projet Data/Feux_USA/Streamlit_projet/Streamlit/streamlit_app.py"


# Visualisation des données PAGE
st.title("Présentation du modèle de prédiction")

# Fonction pour charger les données, avec cache
@st.cache_data
def load_data():
    df = pd.read_csv("/Users/mallou/Documents/Projet Data/Feux_USA/Notebooks/Suppression categorieA/dataset_v2.csv")
    return df

# Charger les données
df = load_data()

#----------------------------------------------------
#1er paragraphe
#----------------------------------------------------
st.header("1- Objectif")

st.subheader("**Créer un modèle capable de prédire les grands feux.**")

st.markdown("Ici, les grands feux représentent les classes minoritaires de la variable **FIRE_SIZE_CLASS** (F et G).\n\n"
            
            "- Pour améliorer les résultats du modèle, nous supprimons la classe A de la variable cible. (FIRE_SIZE_CLASS)\n\n"
            "- Nous regroupons les classes comme suit : \n\n"
            "   **Classe B** = 'small'\n\n"
            "   **Classes C et D** = 'medium'\n\n"
            "   **Classes E, F et G** = 'very_large'\n\n"
            
            "La classe E est rajoutée, pour essayer d'équilibrer les classes pour le modèle."
            
)



#----------------------------------------------------
#2e paragraphe : Suppression des variables
#----------------------------------------------------
st.header("2- Suppression des variables")

st.markdown("À partir du dataset principal concaténé avec les données météorologiques.")

st.markdown("- Variables avec des valeurs manquantes trop importantes \n"
            "- Variables non-nécessaires pour la modélisation \n"
            "- Doublons : Nouvelles variables créées à partir des variables originales")

#----------------------------------------------------
#3e paragraphe : Preprocessing
#----------------------------------------------------
st.header("3- Preprocessing")

st.markdown(f"Après le **'Test/Train/Split'** : ")

#Encodage variable cible
st.markdown("### Encodage de la variable cible")
st.markdown("La variable cible est répartie en 3 catégories : \n\n"
            "**'small'** : 0 (Catégorie B) \n\n"
            "**'medium'** : 1, (Catégories C et D) \n\n"
            "**'very_large'** : 2 (Catégories E, F et G) \n\n")

#Imputation valeurs manquantes
st.markdown("### Imputation sur les valeurs manquantes")
st.markdown("Concerne seulement les variables météorologiques. Entre 2 et 16% de valeurs manquantes")

#Encodage variables catégorielles
st.markdown("### Encodage des variables catégorielles")
st.markdown("**Variables catégorielles ordinales** : Utilisation d'OrdinalEncoder \n\n"
            "**Variables catégorielles nominales (forte cardinalité)** : Utilisation de TargetEncoder \n\n"
            "**Variables catégorielles nominales (faible cardinalité)** : Utilisation de OneHotEncoder \n\n"
)

#----------------------------------------------------
# #4e paragraphe : Modèle Random Forest
#----------------------------------------------------
st.header("4- Modèle & Hyperparamètres")
st.markdown("Après un premier modèle sans paramètre, on effectue une recherche d'hyperparamètres. \n\n"
            "Et ensuite on crée le modèle à l'aide des paramètres trouvés.")
st.subheader("Résultat du 1er modèle avec toutes les variables : ")

#Résultats
st.write("**Score sur ensemble Train :**  0.634431384747863 \n\n"
"**Score sur ensemble Test :**  0.6347755149127975")

# Matrice de confusion en DataFrame
conf_matrix = pd.DataFrame(
    [
        [127663, 53666, 6456],
        [22523, 25024, 2299],
        [2110, 1590, 1380]
    ],
    index=["Classe réelle 0", "Classe réelle 1", "Classe réelle 2"],
    columns=["Classe prédite 0", "Classe prédite 1", "Classe prédite 2"]
)
# Affichage dans Streamlit
st.write("### Matrice de confusion")
st.write(conf_matrix)

# Rapport de classification
report_data = {
    "precision": [0.84, 0.31, 0.14, None, 0.43, 0.72],
    "recall":    [0.68, 0.50, 0.27, None, 0.48, 0.63],
    "f1-score":  [0.75, 0.38, 0.18, 0.63, 0.44, 0.66],
    "support":   [187785, 49846, 5080, 242711, 242711, 242711]
}
index_labels = [
    "Classe 0",
    "Classe 1",
    "Classe 2",
    "Accuracy",
    "Macro avg",
    "Weighted avg"
]

df_report = pd.DataFrame(report_data, index=index_labels)

# Affichage dans Streamlit
st.write("### Rapport de classification")
st.write(df_report)

# Charger l'image depuis le disque
image = Image.open("/Users/mallou/Documents/Projet Data/Feux_USA/PDF/output.png")

# Afficher l'image
st.write("### Importance des variables")
st.image(image, use_container_width=True)



#-------------------------------------
# Sélection 8 variables
#-------------------------------------
st.header("5- Modèle avec 8 variables sélectionnées")

st.markdown("Nous gardons les 8 variables les plus importantes après la création du premier modèle.")

st.markdown("#### **Modèle final :**")

#Résultats
st.write("**Score sur ensemble Train :**  0.642138105003806 \n\n"
"**Score sur ensemble Test :**  0.6421793820634417")


# Matrice de confusion en DataFrame
conf_matrix = pd.DataFrame(
    [
        [130195, 49645, 7945],
        [22890, 24097, 2859],
        [1965, 1543, 1572]
    ],
    index=["Classe réelle 0", "Classe réelle 1", "Classe réelle 2"],
    columns=["Classe prédite 0", "Classe prédite 1", "Classe prédite 2"]
)
# Affichage dans Streamlit
st.write("### Matrice de confusion")
st.write(conf_matrix)

# Rapport de classification
report_data2 = {
    "precision": [0.84, 0.32, 0.13, None, 0.43, 0.72],
    "recall":    [0.69, 0.48, 0.31, None, 0.50, 0.64],
    "f1-score":  [0.76, 0.39, 0.18, 0.64, 0.44, 0.66],
    "support":   [187785, 49846, 5080, 242711, 242711, 242711]
}
index_labels = [
    "Classe 0",
    "Classe 1",
    "Classe 2",
    "Accuracy",
    "Macro avg",
    "Weighted avg"
]

df_report2 = pd.DataFrame(report_data2, index=index_labels)
# Affichage dans Streamlit
st.write("### Rapport de classification")
st.write(df_report2)

# Charger l'image depuis le disque
image2 = Image.open("/Users/mallou/Documents/Projet Data/Feux_USA/PDF/output2.png")

# Afficher l'image
st.write("### Importance des variables")
st.image(image2, use_container_width=True)

st.write("Nous constatons, très peu d'amélioration de la performance du modèle. "
         "Seulement, dans **la matrice confusion**, un gain de 192 observations de plus détecté par le modèle pour la catégorie 'very_large'.")










# Contenu dans la barre côté gauche
st.sidebar.markdown("# Présentation du modèle de prédiction")
st.sidebar.markdown("---")
