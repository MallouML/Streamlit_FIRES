import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import altair as alt
import download_datasets
import os

#streamlit run streamlit_app.py


# Visualisation des données PAGE
st.title("Exploration des données")

# Fonction pour charger les données, avec cache
DATA_DIR = "Datasets"
@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(DATA_DIR, "dataset_v2.csv"))
    return df

# Charger les données
df = load_data()

#--------------------------------------------------------------
#Introduction
#--------------------------------------------------------------
st.markdown("Cette étape dans un projet data, est une étape essentielle pour comprendre la nature du dataset.")

#--------------------------------------------------------------
#1er paragraphe : Vue d'ensemble des feux
#--------------------------------------------------------------
st.header("Vue d'ensemble des feux aux États-Unis")
st.markdown("Dans cette partie, nous allons balayer la représentation des feux dans le paysage américain sur 23 ans.")

#Graphique 1 : Maps des feux aux USA
st.subheader("**1- Carte des feux aux États-Unis entre 1992 et 2015**")

# Renommer pour st.map
df = df.rename(columns={"LATITUDE": "latitude", "LONGITUDE": "longitude"})

# Convertir en float si nécessaire
df["latitude"] = df["latitude"].astype(float)
df["longitude"] = df["longitude"].astype(float)

df = pd.DataFrame(df)
st.map(df)

#--------------------------------------------------------------
#Graphique 2 : Nombre de feux par année sur 23 ans
#--------------------------------------------------------------
st.subheader("**2- Nombre de feux par année**")
st.markdown("#### **2006, 2000, 2007 et 2011**")
st.markdown("Ces 4 années comptabilisent plus de **90 000 feux** sur cette période.")

#Calculs
fire_counts = df['FIRE_YEAR'].value_counts().sort_index()
fire_counts_df = fire_counts.reset_index()
fire_counts_df.columns = ['FIRE_YEAR', 'COUNT']

# Dégradé de rouge
cmap = plt.cm.get_cmap('YlOrRd') 

# Liste des années à mettre en valeur
highlight_years = [2006, 2000, 2007, 2011]

# Fonction pour récupérer une couleur rouge précise
def get_red_color():
    couleur = cmap(0.4) 
    return f"rgb({int(couleur[0]*255)}, {int(couleur[1]*255)}, {int(couleur[2]*255)})"

# Ajouter la colonne couleur
fire_counts_df['color'] = fire_counts_df['FIRE_YEAR'].apply(lambda x: get_red_color() if x in highlight_years else 'grey')

# Créer le graphique Altair
chart = alt.Chart(fire_counts_df).mark_bar().encode(
    x='FIRE_YEAR:O',
    y='COUNT:Q',
    color=alt.Color('color:N', scale=None)
).properties(
    width=700,
    height=400,
    title='Nombre de feux par année'
)

st.altair_chart(chart)

#--------------------------------------------------------------
# Graphique 3 :Les années 2006, 2000, 2007 et 2011
#--------------------------------------------------------------
st.markdown("#### Plus en détail :")
st.markdown("Catégories des feux pour 2006, 2000, 2007, 2011.\n\n "
            "Une très grande domination des feux de la classe A et B, qui correspondent aux feux de taille."
            "\n\n"
            "- A = entre 0 et 0.25 acres (0 à 1 000 m²)" 
            "\n\n"
            "- B = entre 0.26 et 9.9 acres (1 000 m² à 40 000 m² soit 0,04 km²)."
            "\n\n")

#Calculs
annees = [2006, 2000, 2007, 2011]
df_4_ans = df[df['FIRE_YEAR'].isin(annees)]

# Compter le nombre de feux par année et par classe
feux_4_ans_classe = df_4_ans.groupby(['FIRE_YEAR', 'FIRE_SIZE_CLASS']).size().reset_index(name='COUNT')

# Bar chart avec dégradé de rouge
chart = alt.Chart(feux_4_ans_classe).mark_bar().encode(
    x=alt.X('FIRE_YEAR:O', title='Année'),
    y=alt.Y('COUNT:Q', title='Nombre de feux'),
    color=alt.Color('FIRE_SIZE_CLASS:N',
                    scale=alt.Scale(scheme='yelloworangered'),
                    legend=alt.Legend(title="Nombre de feux")),
).properties(
    width=150,
    height=400,
)

st.altair_chart(chart)

#--------------------------------------------------------------
# Graphique 4 : Les États sur 23 ans
#--------------------------------------------------------------
st.subheader("**3- Les États touchés en nombre d'incendies**")
st.markdown("Après avoir comptabilisé, nous regardons quels sont les États les plus touchés en nombre durant la période de 1992 à 2015.")

# Compter les feux par État
feux_par_etat = df['STATE'].value_counts()

# Convertir en DataFrame pour st.bar_chart
feux_par_etat_df = feux_par_etat.reset_index()
feux_par_etat_df.columns = ['STATE', 'COUNT']
fig = px.bar(feux_par_etat_df, 
             x='STATE', 
             y='COUNT', 
             color='COUNT',
             color_continuous_scale='OrRd', 
             text="COUNT")

st.plotly_chart(fig)

#--------------------------------------------------------------
# Graphique 5 :Les États sur 23 ans PETITS FEUX
#--------------------------------------------------------------
st.markdown("#### Plus en détail :")
# Création des onglets variables
a, b = st.tabs(["États touchés par classe A et B", "États touchés parclasse F et G"])

# Classes à analyser
classes_ab = ['A', 'B']
classes_fg = ['F', 'G']

# Filtrer les DataFrames
df_ab = df[df['FIRE_SIZE_CLASS'].isin(classes_ab)]
df_fg = df[df['FIRE_SIZE_CLASS'].isin(classes_fg)]

# Compter le nombre de feux par état
feux_ab_par_etat = df_ab['STATE'].value_counts().reset_index(name='COUNT').head(10)
feux_fg_par_etat = df_fg['STATE'].value_counts().reset_index(name='COUNT').head(10)


with a:
    st.subheader("**États les plus touchés par les feux de classe A et B**")
    st.markdown("Le graphique montre les 10 États les plus touchés par les feux de classe A et B.")
    
    # Afficher les bar charts
    fig_ab = px.bar(
        feux_ab_par_etat,
        x='STATE',
        y='COUNT',
        color='COUNT',
        text='COUNT',
        color_continuous_scale='Reds'
    )

    fig_ab.update_layout(xaxis_title='État', yaxis_title='Nombre de feux')
    st.plotly_chart(fig_ab)

with b:
    st.subheader("**États les plus touchés par les feux de classe F et G**")
    st.markdown("""
    Le graphique montre les 10 États les plus touchés par les feux de classe F et G.
    - F = 4,05 – 20,2 km²
    - G = 20,2 km² et plus
    """)

    fig_fg = px.bar(
        feux_fg_par_etat,
        x='STATE',
        y='COUNT',
        color='COUNT',
        text='COUNT',
        color_continuous_scale='Reds'
    )
    fig_fg.update_layout(xaxis_title='État', yaxis_title='Nombre de feux')
    st.plotly_chart(fig_fg)

#--------------------------------------------------------------
#--------------------------------------------------------------
#2e paragraphe : Répartition géographiques des feux
#--------------------------------------------------------------
#--------------------------------------------------------------
st.header("**Répartition géographiques des feux**")

#--------------------------------------------------------------
#Graphique 1 : Maps des feux aux USA par État et par année
#--------------------------------------------------------------
st.subheader("**1- Carte des départs de feux par État et par année**")
st.markdown('Évolution annuelle de la fréquence des départs de feux de par État')

df_choro = df.groupby(['STATE', 'FIRE_YEAR']).size().reset_index(name='fire_count')

fig_state = px.choropleth(df_choro,
                    locations='STATE',
                    locationmode='USA-states',
                    color='fire_count',
                    animation_frame='FIRE_YEAR',
                    scope='usa',
                    color_continuous_scale='OrRd')

fig.update_layout(geo=dict(lakecolor='rgb(255, 255, 255)'), xaxis_title='État', yaxis_title='Nombre de feux')

st.plotly_chart(fig_state, use_container_width=True)

#--------------------------------------------------------------
#Graphique 2 : Maps des acres brûlés aux USA par État et par année
#--------------------------------------------------------------
st.subheader("**2- Carte de la surface brûlée par État et par année**")

agg_sumfiresYear = df.groupby(['STATE', 'FIRE_YEAR']).agg({'FIRE_SIZE': 'sum'})
agg_sumfiresYear = agg_sumfiresYear.reset_index()

fig_acre = px.choropleth(agg_sumfiresYear,
                    locations='STATE',
                    locationmode='USA-states',
                    color='FIRE_SIZE',
                    animation_frame='FIRE_YEAR',
                    scope='usa',
                    color_continuous_scale='sunset')
fig.update_layout(geo=dict(lakecolor='rgb(255, 255, 255)'), xaxis_title='État', yaxis_title='Nombre de feux')

st.plotly_chart(fig_acre, use_container_width=True)

#--------------------------------------------------------------
#--------------------------------------------------------------
#3e paragraphe : Raisons des départs de feux
#--------------------------------------------------------------
#--------------------------------------------------------------
st.header("**Les facteurs de départs de feux**")

#--------------------------------------------------------------
#Thème 1 : CAUSES
#--------------------------------------------------------------

#--------------------------------------------------------------
#Graphique 1 : les causes au global
#--------------------------------------------------------------
st.subheader("Ensemble des causes d'un départ de feu")

st.write("Sur l'ensemble des feux enregistrés, **la cause d'origine humaine** est la première responsable.")

# Création de la nouvelle colonne
col0, col1 = st.columns(2, border=True)

#--------------------------------------------------------------
#1ère colonne
#--------------------------------------------------------------

# Dictionnaire de mapping
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

df['CAUSE_GROUP'] = df['STAT_CAUSE_DESCR'].map(cause_mapping)
cause_counts = df['CAUSE_GROUP'].value_counts()

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

#--------------------------------------------------------------
#2e colonne
#--------------------------------------------------------------
col1.subheader("Causes détaillées par groupe")

#Description des causes regroupées
Humaines = []
Naturelles = []
Infrastructure = []
Autres = []

for cause, group in zip(df['STAT_CAUSE_DESCR'], df['CAUSE_GROUP']):
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

#--------------------------------------------------------------
#Superficie brûlée (lightning)
#--------------------------------------------------------------
#Graphique 1 : les causes par surface brûlée
st.subheader("Surfaces brûlées par cause")

st.write(""" Bien que les incendies de cause naturelle ne rerésentent que près de **15%** des incendies sur 23 ans,
         un incendie provoqué par la cause 'lightning' (la foudre) a fait **62 % des dégâts** au total. (87 033 501 acres brûlés sur 140 millions acres.)
         """)

acres_burned = df.groupby('STAT_CAUSE_DESCR')['FIRE_SIZE'].sum().sort_values(ascending=False)

fig_acre_cause = px.bar(
        x=acres_burned.index,
        y=acres_burned.values,
        text=acres_burned.values,
        labels={'x': 'Catégorie de cause', 'y': 'Surfaces brûlées'},
        color=acres_burned.index,
        color_discrete_sequence=px.colors.qualitative.Set2
    )

fig_acre_cause.update_traces(textposition='outside')
fig_acre_cause.update_layout(showlegend=False, height=500)

st.plotly_chart(fig_acre_cause, use_container_width=True)















# Contenu dans la barre côté gauche
st.sidebar.markdown("# Visualisation des données")
st.sidebar.markdown("---")
