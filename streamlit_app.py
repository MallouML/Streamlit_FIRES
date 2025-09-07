import streamlit as st
#streamlit run streamlit_app.py

# TITLE, TEAM_MEMBERS and PROMOTION values in config.py.
import config

import download_datasets

# Télécharge les fichiers si nécessaire
download_datasets.download_datasets()

# Define the pages
main_page = st.Page("main_page.py", title="Bienvenue")
page_1 = st.Page("page_1.py", title="Présentation des données")
page_2 = st.Page("page_2.py", title="Exploration des données")
page_3 = st.Page("page_3.py", title="Zoom : les États les plus touchés")
page_4 = st.Page("page_4.py", title="Présentation du modèle de prédiction")
page_5 = st.Page("page_5.py", title="Prédiction de la classe d'un feu")
page_6 = st.Page("page_6.py", title="Perspectives d'évolution")

# Set up navigation
pg = st.navigation([main_page, page_1, page_2, page_3, page_4, page_5, page_6])

# Run the selected page
pg.run()

st.sidebar.markdown("### Team members:")
for member in config.TEAM_MEMBERS:
    st.sidebar.markdown(member.sidebar_markdown(), unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown(f"## {config.PROMOTION}")
