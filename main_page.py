import streamlit as st
#/Users/mallou/Documents/Projet\ Data/Feux_USA/.conda/bin/streamlit run "/Users/mallou/Documents/Projet Data/Feux_USA/Streamlit/streamlit_app.py"

# TITLE, TEAM_MEMBERS and PROMOTION values in config.py.
import config

st.header("🔥 Introduction")

st.info("Projet de fin de formation : **Analyse & Prédiction des Feux de Forêt aux États-Unis (1992–2015)**")

st.markdown("""
### 🎬 Accroche
- Été **2006** : **114 000 incendies** → plus de **300 par jour**
- Destruction de millions d’hectares, familles évacuées, milliards $ dépensés
- Un enjeu **humain**, **écologique** et **économique**
""")

st.divider()

st.markdown("""
### ⚖️ Le paradoxe métier
- **85 %** des feux sont d’**origine humaine**
- La majorité des feux sont de **petites flammes vite éteintes**
- Mais **2,8 %** concentrent près de **70 % des dégâts**
👉 Le vrai défi : **repérer très tôt** les feux à haut potentiel destructeur
""")

st.divider()

st.markdown("""
### 🚀 Notre mission
- Explorer **1,88 million** d’incendies documentés sur **24 ans**
- **Enrichir** chaque feu avec la **météo au moment T0**
- Construire un **outil prédictif interactif** pour soutenir la décision
""")

st.markdown("""
### ❓ Question clé
> *Peut-on prédire, dès son **ignition**, si un feu restera **mineur** ou deviendra **majeur** ?*
""")

st.divider()

st.markdown("""
### 📌 Ce que vous allez découvrir
1. **EDA & Insights** : où, quand et pourquoi les USA brûlent
2. **Démo interactive** : visualiser, filtrer et prédire un feu en conditions réelles
3. **Impact métier** : comment mieux **prépositionner les moyens**
""")

st.caption("✨ *Chaque feu raconte une histoire… la donnée peut aider à en prédire l’issue.*")




# Contenu dans la barre côté gauche
st.sidebar.markdown("# Bienvenue")
st.sidebar.markdown("---")
