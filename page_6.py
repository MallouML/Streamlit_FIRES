import streamlit as st
import pandas as pd

#streamlit run streamlit_app.py

# Titre
st.title("Perspectives d'évolution")

st.header("**3 améliorations :**")
st.subheader("1- Qualité des données")
st.markdown("- Les valeurs manquantes de variables potentiellement intéressantes\n"
            "- Trouver des données de 2015 à maintenant\n"
            "- Creuser sur les mégafeux (Beaucoup plus fréquent après 2015)\n")

st.subheader("2- Données supplémentaires")
st.markdown("- Données coûts liés aux dégâts des feux (Équipes d'intervention, matériels, humaines etc)\n"
            "- Données socio-économiques\n"
            "- Données réponde et gestion des feux\n"
            "- Données conséquences écologiques")

st.subheader("3- Amélioration du modèle de Machine-Learning")
st.markdown("- Choix du modèle\n"
            "- L'importance des variables\n"
            "- Les hyperparamètres\n")

st.header("**Pour aller plus loin :**")
st.subheader("1- Sensibiliser et gestion des risques")
st.markdown("- **Renforcer la surveillance :** Arriver à détecter plus tôt les départs de feux.\n"
            "- **Améliorer la gestion des forêts :** programmes de brûlages contrôlés, débroussaillage et réduction des combustibles naturels.\n")

st.subheader("2- Sensibilisation et politiques publics")
st.markdown("- **Sensibiliser et former :** les habitants des zones à risque.\n"
            "- **Améliorer les réglementations strictes** déjà en place lors des périodes critiques.\n"
            "- Plus de considération du secteur public pour les équipes d'intervention (financières, humaines et matérielles)\n")

