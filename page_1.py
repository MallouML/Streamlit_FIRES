import streamlit as st
import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt 
import plotly.express as px

df1, df2 = load_data()


# Exploration des données PAGE
st.title("Présentation des données")

#https://github.com/streamlit/docs/blob/main/python/concept-source/theming-overview-anthropic-light-inspried/layouts.py

#1er paragraphe datasets
st.header("Présentation des datasets")
st.markdown("Vous trouverez ci-dessous les 2 datasets")



# Création des onglets datasets
#a, b, c = st.tabs(["Dataset principal", "Dataset météorologiques", "Dataset population"])
a, b = st.tabs(["Dataset principal", "Dataset météorologiques"])

with a:
    st.write("Voici le premier dataset :")
    st.dataframe(df1.head(100))
    choice = st.pills("Détails", 
                      options=["Taille DataFrame", "Description", "Valeurs manquantes"],
                      key="pills_df1" )

    if choice == "Taille DataFrame":
        st.write(f"Le DataFrame contient **{df1.shape[0]} lignes** et **{df1.shape[1]} colonnes**.")
    
    elif choice == "Description":
        st.write("Résumé statistique :")
        st.dataframe(df1.describe(include='all'))
    
    elif choice == "Valeurs manquantes":
        st.write("Nombre de valeurs manquantes par colonne :")
        def missing_values_table(df1):
            total = df1.isnull().sum()
            percent = (total / len(df1)) * 100
            missing_df = pd.DataFrame({
                "Nombre de valeurs manquantes": total,
                "Pourcentage (%)": percent
            })
            missing_df = missing_df[missing_df["Nombre de valeurs manquantes"] > 0]
            return missing_df.sort_values("Pourcentage (%)", ascending=False)
        st.write("### Valeurs manquantes par colonne")
        st.dataframe(missing_values_table(df1))


with b:
    st.write("Voici le deuxième dataset :")
    st.dataframe(df2.head(100))
    choice = st.pills("Détails", options=["Taille DataFrame", "Description", "Valeurs manquantes"],
                      key="pills_df2" )

    if choice == "Taille DataFrame":
        st.write(f"Le DataFrame contient **{df2.shape[0]} lignes** et **{df2.shape[1]} colonnes**.")
    
    elif choice == "Description":
        st.write("Résumé statistique :")
        st.dataframe(df2.describe(include='all'))
    
    elif choice == "Valeurs manquantes":
        st.write("Nombre de valeurs manquantes par colonne :")
        def missing_values_table2(df2):
            total2 = df2.isnull().sum()
            percent2 = (total2 / len(df2)) * 100
            missing_df2 = pd.DataFrame({
                "### Nombre de valeurs manquantes": total2,
                "Pourcentage (%)": percent2
            })
            missing_df2 = missing_df2[missing_df2["Nombre de valeurs manquantes"] > 0]
            return missing_df2.sort_values("Pourcentage (%)", ascending=False)
        st.write("#### Valeurs manquantes par colonne")
        st.dataframe(missing_values_table2(df2))
    
st.markdown("___________________________________________")

#2e paragraphe datasets
st.header("Présentation des variables")
st.markdown("Vous trouverez ci-dessous les variables des 2 datasets.")
st.warning("Les types des variables que vous voyez, sont les types d'origine.\n")


# Création des onglets variables
d, e = st.tabs(["Variables dataset principal", "Variables dataset météorologiques"])

with d:
    st.write("Voici les variables du premier dataset :")
    st.markdown("""
    | Champ                      | Type     | Description                                                                 |
    |-----------------------------|----------|-----------------------------------------------------------------------------|
    | OBJECTID                   | int64    | Identifiant unique                                                          |
    | FPA_ID                     | object   | ID FPA (Fire Program Analysis)                                              |
    | SOURCE_SYSTEM_TYPE         | object   | Type de système source                                                      |
    | SOURCE_SYSTEM              | object   | Système source                                                              |
    | NWCG_REPORTING_AGENCY      | object   | Agence de rapport NWCG                                                      |
    | NWCG_REPORTING_UNIT_ID     | object   | ID unité de rapport NWCG                                                    |
    | NWCG_REPORTING_UNIT_NAME   | object   | Nom de l'unité de rapport NWCG                                              |
    | SOURCE_REPORTING_UNIT      | object   | Unité source de rapport                                                     |
    | SOURCE_REPORTING_UNIT_NAME | object   | Nom de l'unité source de rapport                                            |
    | LOCAL_FIRE_REPORT_ID       | object   | ID local de rapport d'incendie                                              |
    | LOCAL_INCIDENT_ID          | object   | ID local d'incident                                                         |
    | FIRE_CODE                  | object   | Code de feu                                                                 |
    | FIRE_NAME                  | object   | Nom du feu                                                                  |
    | ICS_209_INCIDENT_NUMBER    | object   | Numéro d'incident ICS-209                                                   |
    | ICS_209_NAME               | object   | Nom ICS-209                                                                 |
    | MTBS_ID                    | object   | ID MTBS (Monitoring Trends in Burn Severity)                                |
    | MTBS_FIRE_NAME             | object   | Nom du feu MTBS                                                             |
    | COMPLEX_NAME               | object   | Nom du complexe (d'incendies)                                               |
    | FIRE_YEAR                  | int64    | Année du feu                                                                |
    | DISCOVERY_DATE             | float64  | Date de découverte                                                          |
    | DISCOVERY_DOY              | int64    | Jour de l'année de découverte                                               |
    | DISCOVERY_TIME             | float64  | Heure de découverte                                                         |
    | STAT_CAUSE_CODE            | float64  | Code de cause statistique                                                   |
    | STAT_CAUSE_DESCR           | object   | Description de la cause statistique                                         |
    | CONT_DATE                  | float64  | Date de maîtrise                                                            |
    | CONT_DOY                   | float64  | Jour de l'année de maîtrise                                                 |
    | CONT_TIME                  | float64  | Heure de maîtrise                                                           |
    | FIRE_SIZE                  | float64  | Taille du feu (en acres)                                                   |
    | FIRE_SIZE_CLASS            | object   | Classe de taille du feu                                                     |
    | LATITUDE                   | float64  | Latitude                                                                    |
    | LONGITUDE                  | float64  | Longitude                                                                   |
    | OWNER_CODE                 | float64  | Code du propriétaire terrien                                                |
    | OWNER_DESCR                | object   | Description du propriétaire terrien                                         |
    | STATE                      | object   | État (USA)                                                                  |
    | COUNTY                     | object   | Comté : un niveau de gouvernement local et une division territoriale intermédiaire entre les États fédérés et les villes ou municipalités |
    | FIPS_CODE                  | float64  | Code FIPS (Federal Information Processing Standards)                        |
    | FIPS_NAME                  | object   | Nom FIPS                                                                    |
    | Shape                      | object   | Géométrie (shapefile)                                                       |
    """)

    


with e:
    st.write("Voici les variables du deuxième dataset :")
    st.markdown("""
    | Champ          | Type     | Description                                                                 |
    |----------------|----------|-----------------------------------------------------------------------------|
    | temp_mean_0    | float64  | Température moyenne (°C) le jour de l’incendie                              |
    | prcp_sum_0     | float64  | Précipitations totales (mm) le jour de l’incendie                           |
    | wspd_mean_0    | float64  | Vitesse moyenne du vent (km/h) le jour de l’incendie                        |
    | temp_mean_10   | float64  | Température moyenne (°C) pendant les 10 jours précédant l’incendie          |
    | prcp_sum_10    | float64  | Précipitations totales (mm) pendant les 10 jours précédant l’incendie       |
    | wspd_mean_10   | float64  | Vitesse moyenne du vent (km/h) pendant les 10 jours précédant l’incendie    |
    | temp_mean_30   | float64  | Température moyenne (°C) pendant les 30 jours précédant l’incendie          |
    | prcp_sum_30    | float64  | Précipitations totales (mm) pendant les 30 jours précédant l’incendie       |
    | wspd_mean_20   | float64  | Vitesse moyenne du vent (km/h) **20 jours** précédant l’incendie            |
    | temp_mean_60   | float64  | Température moyenne (°C) pendant les 60 jours précédant l’incendie          |
    | prcp_sum_60    | float64  | Précipitations totales (mm) pendant les 60 jours précédant l’incendie       |
    | wspd_mean_60   | float64  | Vitesse moyenne du vent (km/h) pendant les 60 jours précédant l’incendie    |
    | temp_mean_180  | float64  | Température moyenne (°C) pendant les 180 jours précédant l’incendie         |
    | prcp_sum_180   | float64  | Précipitations totales (mm) pendant les 180 jours précédant l’incendie      |
    | wspd_mean_180  | float64  | Vitesse moyenne du vent (km/h) pendant les 180 jours précédant l’incendie   |
    | OBJECTID       | int64    | Identifiant unique                                                          |
    """)




# Contenu dans la barre côté gauche
st.sidebar.markdown("# Exploration des données")
st.sidebar.markdown("---")
