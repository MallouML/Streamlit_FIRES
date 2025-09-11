import streamlit as st
import pandas as pd
import plotly.express as px 
import os

#streamlit run streamlit_app.py


# Visualisation des données PAGE
st.title("Zoom : les États les plus touchés")

# Fonction pour charger les données, avec cache
@st.cache_data
def load_data():
    base_path = os.path.join(os.path.dirname(__file__), "Datasets")
    df = pd.read_csv(os.path.join(base_path, "dataset_v2.csv"))
    return df

# Charger les données
df = load_data()

#Introduction
st.markdown("Ici, nous allons nous concentrer sur les États les plus touchés en nombre et en superficie brûlées.")

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#1er paragraphe : Les États avec un nombre de feux IMP
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
st.header("1- Zoom sur les États les plus touchés en nombre.")

#------------------------------------------------------------------------------------------------------
#Graphique 1 : Maps des feux aux USA
#------------------------------------------------------------------------------------------------------
st.markdown("Un aperçu des 8 États avec un nombre de feux représentant la moitié du total sur 23 ans.")

# Top 8 États les plus touchés (en nombre de feux)
states8 = df['STATE'].value_counts().head(8).reset_index()
states8.columns = ['STATE', 'Nombre']

# Calcul du pourcentage
states8['Pourcentage'] = (states8['Nombre'] / len(df)) * 100
states8['Pourcentage_cumulé'] = states8['Pourcentage'].cumsum()

# Arrondir le pourcentage pour un affichage plus propre
states8['Pourcentage'] = states8['Pourcentage'].round(2)

# Affichage dans Streamlit
st.markdown("### Top 8 des États les plus touchés par les feux")
st.dataframe(states8, use_container_width=True)

# afficher la couverture totale du top 8
coverage = (states8['Nombre'].sum() / len(df)) * 100
st.markdown(f"**Les 8 États représentent {coverage:.2f}% de tous les feux.**")
st.markdown("Nous allons regarder plus en détail les 8 États.")


abbr_to_state_feux = {
    "CA": "California",
    "GA": "Georgia",
    "TX": "Texas",
    "NC": "North Carolina",
    "FL": "Florida",
    "SC": "South Carolina",
    "NY": "New York",
    "MS": "Mississippi"
}

cause_mapping = {
    'Debris Burning': 'Humaine',
    'Miscellaneous': 'Humaine',
    'Lightning': 'Naturelle',
    'Arson': 'Humaine',
    'Missing/Undefined': 'Autres',
    'Equipment Use': 'Infrastructure',
    'Campfire': 'Humaine',
    'Children': 'Humaine',
    'Smoking': 'Humaine',
    'Railroad': 'Infrastructure',
    'Powerline': 'Infrastructure',
    'Fireworks': 'Humaine',
    'Structure': 'Infrastructure'
}

region_tooltips = {
    "California": (
        "Californie (PACIFIC) : Climat méditerranéen, zones côtières, forêts et montagnes. "
    ),
    "Georgia": (
        "Géorgie (SOUTH_ATLANTIC) : Climat subtropical humide, plaines côtières, forêts. "
    ),
    "Texas": (
        "Texas (WEST_SOUTH_CENTRAL) : Climat varié, incluant prairies, déserts et zones forestières. "
    ),
    "North Carolina": (
        "Caroline du Nord (SOUTH_ATLANTIC) : Climat subtropical humide, plages, collines, montagnes. "
    ),
    "Florida": (
        "Floride (SOUTH_ATLANTIC) : Climat subtropical humide, plages, marécages. "
    ),
    "South Carolina": (
        "Caroline du Sud (SOUTH_ATLANTIC) : Climat subtropical humide, plages, forêts. "
    ),
    "New York": (
        "New York (MID_ATLANTIC) : Climat continental humide, montagnes, lacs. "
    ),
    "Mississippi": (
        "Mississippi (SOUTH_EAST_CENTRAL) : Climat subtropical humide, forêts, marécages. "
    )
}


tooltip_vegetation = {
    "California": (
        "Californie : Variés, forêts, chaparral, désert, zones côtières. "
    ),
    "Georgia": (
        "Géorgie : Forêts de feuillus et pins du Sud, zones humides et plaines. "
    ),
    "Texas": (
        "Texas : Prairies, zones désertiques, forêts et côtes du Golfe. "
    ),
    "North Carolina": (
        "Caroline du Nord : Forêts de feuillus, montagnes des Appalaches et zones côtières. "
    ),
    "Florida": (
        "Floride : Everglades, mangroves et forêts subtropicales. "
    ),
    "South Carolina": (
        "Caroline du Sud : Forêts subtropicales et zones côtières de l'Atlantique. "
    ),
    "New York": (
        "New York : Forêts tempérées de feuillus, montagnes et lacs, y compris les Adirondacks. "
    ),
    "Mississippi": (
        "Mississippi : Forêts de feuillus et pins du Sud, zones humides. "
    )
}





# Liste des États sélectionnables
etats_nb = ["California", "Georgia", "Texas", "North Carolina", 
         "Florida", "South Carolina", "New York", "Mississippi"]

# Sélecteur
etat_selectionne = st.segmented_control("États :", etats_nb, default="California")

# Filtrer les données pour l'État choisi
df_etat = df[df['STATE'].map(abbr_to_state_feux) == etat_selectionne]

#------------------------------------------------------------------------------------------------------
#Métriques
#------------------------------------------------------------------------------------------------------
# Métriques liées au nombre de feux 
nombre_feux = df_etat['FIRE_SIZE'].count()
pourcentage_feux = (nombre_feux / df['FIRE_SIZE'].count()) * 100  

# Classement par nombre de feux
states_count = df['STATE'].value_counts().reset_index()
states_count.columns = ['STATE', 'Nombre_de_feux']
states_count['Classement'] = states_count['Nombre_de_feux'].rank(method='min', ascending=False)
classement = int(states_count[states_count['STATE'] == df_etat['STATE'].iloc[0]]['Classement'])

# Métrique Région
region = df_etat['REGION'].mode()[0]

#Métrique végétation
vegetation = df_etat['Type_1'].mode()[0]

#------------------------------------------------------------------------------------------------------
# Carte des feux
#------------------------------------------------------------------------------------------------------
df_map = df_etat[['LATITUDE', 'LONGITUDE']].dropna()
st.map(df_map)

st.markdown("\n\n")

# Affichage des métriques
cols1 = st.columns(2)
cols1[0].metric("État sélectionné", etat_selectionne, border=True)
cols1[1].metric("Nombre de feux", f"{nombre_feux:,}", border=True)

cols2 = st.columns(2)
cols2[0].metric("Pourcentage du total des feux", f"{pourcentage_feux:.2f}%", border=True)
cols2[1].metric("Classement par nombre de feux", f"{classement}", border=True)

cols3 = st.columns(2)
cols3[0].metric("Région", 
                f"{region}", 
                border=True,
                help=region_tooltips.get(etat_selectionne, "Région de l'État."))
cols3[1].metric("Végétation principale", 
                f"{vegetation}", 
                border=True,
                 help=tooltip_vegetation.get(etat_selectionne, "Information végétation non disponible")
)

st.markdown("\n\n")

#------------------------------------------------------------------------------------------------------
#Graphique classes des feux
#------------------------------------------------------------------------------------------------------
classe_fire = df_etat['FIRE_SIZE_CLASS'].value_counts()
st.bar_chart(classe_fire)

st.markdown("\n\n")

#------------------------------------------------------------------------------------------------------
#Graphique des causes 
#------------------------------------------------------------------------------------------------------
# Création de la nouvelle colonne
col0, col1 = st.columns(2, border=True)

df_etat['CAUSE_GROUP'] = df_etat['STAT_CAUSE_DESCR'].map(cause_mapping)

cause_counts = df_etat['CAUSE_GROUP'].value_counts()

fig_pl = px.bar(
        x=cause_counts.index,
        y=cause_counts.values,
        text=cause_counts.values,
        labels={'x': 'Catégorie de cause', 'y': 'Nombre de feux'},
        color=cause_counts.index,
        color_discrete_sequence=px.colors.qualitative.Set2
    )

fig_pl.update_traces(textposition='outside')
fig_pl.update_layout(showlegend=False, height=500)

col0.plotly_chart(fig_pl, use_container_width=True)
#2e colonne
col1.subheader("Causes détaillées par groupe")

#Description des causes regroupées
Humaines = []
Naturelles = []
Infrastructure = []
Autres = []

for cause, group in zip(df_etat['STAT_CAUSE_DESCR'], df_etat['CAUSE_GROUP']):
    if group == 'Humaine':
        Humaines.append(cause)
    elif group == 'Naturelle':
        Naturelles.append(cause)
    elif group == 'Infrastructure':
        Infrastructure.append(cause)
    else:
        Autres.append(cause)

col1.write("**Humaine :** "+", ".join(set(Humaines)))
col1.write("**Naturelle :** "+", ".join(set(Naturelles)))
col1.write("**Infrastructure :** "+", ".join(set(Infrastructure)))
col1.write("**Autres :** "+", ".join(set(Autres)))

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#2e paragraphe : Les États avec une surface brulée IMP
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
st.header("2- Zoom sur les États les plus touchés en superficie brûlées.")

#------------------------------------------------------------------------------------------------------
#Graphique 1 : DF des feux aux USA
#------------------------------------------------------------------------------------------------------
st.markdown("Un aperçu des 6 États avec une superficie brûlée représentant plus de la moitié du pays sur 23 ans.")

# Somme des surfaces brûlées par État
states_size = df.groupby('STATE')['FIRE_SIZE'].sum().reset_index()

# Renommer les colonnes
states_size.columns = ['STATE', 'Surface_brulee']

# Trier par surface brûlée décroissante
states_size = states_size.sort_values(by='Surface_brulee', ascending=False)

# Ajouter le pourcentage
total = states_size['Surface_brulee'].sum()
states_size['Pourcentage'] = (states_size['Surface_brulee'] / total) * 100
states_size['Pourcentage_cum'] = states_size['Pourcentage'].cumsum()

# Garder les 6 premiers États
top6_states = states_size.head(6)

# Affichage dans Streamlit
st.markdown("### Top 6 des États les plus touchés en superficie")
st.dataframe(top6_states, use_container_width=True)

# afficher la couverture totale du top 6
coverage_6 = top6_states['Surface_brulee'].sum() / total * 100
st.markdown(f"**Les 6 États représentent {coverage_6:.2f}% de tous les feux.**")
st.markdown("Nous allons regarder plus en détail les 6 États.")


abbr_to_state = {
    "AK": "Alaska",
    "ID": "Idaho",
    "CA": "California",
    "TX": "Texas",
    "NV": "Nevada",
    "OR": "Oregon"
}

cause_mapping = {
    'Debris Burning': 'Humaine',
    'Miscellaneous': 'Humaine',
    'Lightning': 'Naturelle',
    'Arson': 'Humaine',
    'Missing/Undefined': 'Autres',
    'Equipment Use': 'Infrastructure',
    'Campfire': 'Humaine',
    'Children': 'Humaine',
    'Smoking': 'Humaine',
    'Railroad': 'Infrastructure',
    'Powerline': 'Infrastructure',
    'Fireworks': 'Humaine',
    'Structure': 'Infrastructure'
}

region_tooltips2 = {
    "Alaska": (
        "Alaska (PACIFIC) : Le plus grand État des États-Unis, avec montagnes, glaciers et forêts boréales. "
        "Climat subarctique à arctique, hivers très froids, étés frais."
    ),
    "Idaho": (
        "Idaho (MOUNTAIN) : État montagneux avec vastes forêts et collines. "
        "Climat continental, hivers froids et étés doux."
    ),
    "California": (
        "Californie (PACIFIC) : Climat méditerranéen, zones côtières, forêts et montagnes. "
        "Étés secs, hivers doux, désert dans le sud-est."
    ),
    "Texas": (
        "Texas (WEST_SOUTH_CENTRAL) : Grandes plaines, forêts et zones désertiques. "
        "Climat très variable, étés chauds, hivers doux."
    ),
    "Nevada": (
        "Nevada (MOUNTAIN) : État désertique et montagneux, incluant la Sierra Nevada. "
        "Climat aride à semi-aride, étés chauds et hivers froids."
    ),
    "Oregon": (
        "Oregon (PACIFIC) : Forêts denses, montagnes et zones côtières. "
        "Climat tempéré humide à l’ouest, semi-aride à l’est, hivers doux, étés modérés."
    )
}



tooltip_vegetation1 = {
    "Alaska": (
        "Alaska : Toundra et forêts boréales, montagnes et glaciers. "
    ),
    "Idaho": (
        "Idaho : Montagnes, forêts de conifères et prairies alpines. "
    ),
    "California": (
        "Californie : Divers – forêts, chaparral, désert, zones côtières. "
    ),
    "Texas": (
        "Texas : Prairies, zones désertiques, forêts et côtes du Golfe. "
    ),
    "Nevada": (
        "Nevada : Désert et montagnes, incluant le Grand Bassin. "
    ),
    "Oregon": (
        "Oregon : Forêts de conifères, montagnes et zones côtières. "
    )
}



# Liste des États sélectionnables
etats = ["Alaska", "Idaho", "California", "Texas", 
         "Nevada", "Oregon"]

# Sélecteur
etat_selectionne = st.segmented_control("États :", etats, default="Alaska")

# Filtrer les données pour l'État choisi
# Attention : si df['STATE'] contient des abréviations, il faudra convertir en noms complets
df_etat_superficie = df[df['STATE'].map(abbr_to_state) == etat_selectionne]

# df_etat  filtré pour l'État choisi
nombre_feux = df_etat_superficie['FIRE_SIZE'].count()
surface_totale = df_etat_superficie['FIRE_SIZE'].sum()
pourcentage_total = (surface_totale / df['FIRE_SIZE'].sum()) * 100

# Classement par superficie brûlée 
states_size = df.groupby('STATE')['FIRE_SIZE'].sum()
states_sorted = states_size.sort_values(ascending=False).reset_index()
states_sorted['Classement'] = states_sorted['FIRE_SIZE'].rank(method='min', ascending=False)

# Trouver le classement de l'État sélectionné
classement = int(states_sorted[states_sorted['STATE'] == df_etat_superficie['STATE'].iloc[0]]['Classement'])

#------------------------------------------------------------------------------------------------------
# Carte des feux
#------------------------------------------------------------------------------------------------------
df_map = df_etat_superficie[['LATITUDE', 'LONGITUDE']].dropna()
st.map(df_map)

st.markdown("\n\n")

#------------------------------------------------------------------------------------------------------
#Métriques
#------------------------------------------------------------------------------------------------------
# Métrique Région
region = df_etat_superficie['REGION'].mode()[0]

#Métrique végétation
vegetation = df_etat_superficie['Type_1'].mode()[0]

# Affichage métriques 
cols1 = st.columns(2)

cols1[0].metric("Nombre de feux", f"{nombre_feux:,}", border=True)
cols1[1].metric("Surface brûlée (acres)", f"{surface_totale:,.0f}", border=True)

cols2 = st.columns(2)
cols2[0].metric("Pourcentage du total du pays", f"{pourcentage_total:.2f}%", border=True)
cols2[1].metric("Classement par superficie", f"{classement}", border=True)

cols3 = st.columns(2)
cols3[0].metric("Région", 
                f"{region}", 
                border=True,
                help=region_tooltips2.get(etat_selectionne, "Région de l'État."))
cols3[1].metric("Végétation principale", 
                f"{vegetation}", 
                border=True,
                 help=tooltip_vegetation1.get(etat_selectionne, "Information végétation non disponible")
)

st.markdown("\n\n")

#------------------------------------------------------------------------------------------------------
#Graphique classes des feux
#------------------------------------------------------------------------------------------------------
classe_fire = df_etat['FIRE_SIZE_CLASS'].value_counts()
st.bar_chart(classe_fire)

st.markdown("\n\n")

#------------------------------------------------------------------------------------------------------
#Graphique des causes 
#------------------------------------------------------------------------------------------------------
# Création de la nouvelle colonne
col0, col1 = st.columns(2, border=True)

df_cause = cause_counts.reset_index()
df_cause.columns = ['Cause', 'Nombre']

# Graphique Plotly
fig_pl = px.bar(
    df_cause,
    x='Cause',
    y='Nombre',
    text='Nombre',
    labels={'Cause': 'Catégorie de cause', 'Nombre': 'Nombre de feux'},
    color='Cause',
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig_pl.update_traces(textposition='outside')
fig_pl.update_layout(showlegend=False, height=500)
col0.plotly_chart(fig_pl, use_container_width=True)

#2e colonne
col1.subheader("Causes détaillées par groupe")

#Description des causes regroupées
Humaines = []
Naturelles = []
Infrastructure = []
Autres = []

for cause, group in zip(df_etat['STAT_CAUSE_DESCR'], df_etat['CAUSE_GROUP']):
    if group == 'Humaine':
        Humaines.append(cause)
    elif group == 'Naturelle':
        Naturelles.append(cause)
    elif group == 'Infrastructure':
        Infrastructure.append(cause)
    else:
        Autres.append(cause)

col1.write("**Humaine :** "+", ".join(set(Humaines)))
col1.write("**Naturelle :** "+", ".join(set(Naturelles)))
col1.write("**Infrastructure :** "+", ".join(set(Infrastructure)))
col1.write("**Autres :** "+", ".join(set(Autres)))










# Contenu dans la barre côté gauche
st.sidebar.markdown("# Zoom sur les États les plus touchés")
st.sidebar.markdown("---")
