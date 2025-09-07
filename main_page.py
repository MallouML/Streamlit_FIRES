import streamlit as st
#streamlit run streamlit_app.py

# TITLE, TEAM_MEMBERS and PROMOTION values in config.py.
import config

#Trouver thème couleur en rouge

# Main page content
st.title("Prédire la classe des feux aux États-Unis")
st.header("Bienvenue sur notre projet de l'analyse des feux aux États-Unis. ")
st.subheader("**140 132 549 acres**")

st.markdown("Ce chiffre représente la surface brûlée entre 1922 et 2015 par les feux (environ 567 096 km2) aux États-Unis. Presque que l'équivalent de l'État du Texas.")

st.markdown("**La mission :** À travers la compréhension des feux, être en mesure de prévenir et de prédire les futurs feux dans le futur.")

#Paragraphe Contexte
st.header("Objectif du projet")
st.markdown("Des paysages désertiques du monument valley en Arizona, "
            "aux régions montagneuses des Fours Corners, puis jusqu'aux côtes tropicales de Floride, sans oublier les territoires singuliers comme l'Alaska, Hawaï et Puerto Rico, "
            "les États-Unis offrent une remarquable diversité de climats, de régions et de forêts.")
st.subheader("**1,88 millions de feux**")
st.markdown("Soit 220 incendies par jour pendant 23 ans. Derrière ces chiffres impressionnants, nous allons chercher à comprendre "
            "quels sont les facteurs qui favorisent le départ d'un feu, qui peut être de toute nature (temporelle, géographique etc).")

#Paragraphe origine des données
st.header("Origine des données")
#st.markdown("### Le jeu de données principale ")
st.subheader("Le jeu de données principale ")
st.markdown("C'est une base de données spatiale des incendies de forêts survenus aux États-Unis entre 1992 et 2015, avec la licence CC0. "
            "\n C'est-à-dire qu'il est disponible intégralement dans le domaine public avec la libre modification des données. "
            "\n\n"
            "Possibilité de le récupérer sur kaggle."
            "\n\n"
            "**Lien :** https://www.kaggle.com/datasets/rtatman/188-million-us-wildfires"
            )

#st.markdown("### Jeu de données météorologiques")
st.subheader("Jeu de données météorologiques")
st.markdown("Ce dataset survient directement du dataset principal, où chaque feu est décrit avec sa température, le vent les précipitations (J0, J-10, J-30, J-60, J-180). "
            "\n\n"
            "Également disponible sur kaggle. "
            "\n\n"
            "**Lien :** https://www.kaggle.com/datasets/leternnoz/188-million-us-wildfires-weather-data")

#st.markdown("### Jeu de données population")
st.subheader("Jeu de données population")
st.markdown("Ce dataset a été créé à partir de . "
            "\n\n")






# Contenu dans la barre côté gauche
st.sidebar.markdown("# Page principale")
st.sidebar.markdown("---")