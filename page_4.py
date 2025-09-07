import streamlit as st
import pandas as pd
from PIL import Image


#streamlit run streamlit_app.py


# Visualisation des données PAGE
st.title("Présentation du modèle de prédiction")

# Fonction pour charger les données, avec cache
@st.cache_data
def load_data():
    df = pd.read_csv("/Users/mallou/Documents/Projet Data/Streamlit_fires/Streamlit/Datasets/dataset_v2.csv")
    return df

# Charger les données
df = load_data()

#1er paragraphe
st.header("1- Choix des variables")

st.markdown("À partir du dataset concaténer avec les données météorologiques")
st.markdown("- Valeurs manquantes trop importantes \n"
            "- Valeurs de l'attributs non nécessaires pour la modélisation")
st.markdown("Pour la création du modèle de Machine Learning, nous décidons d'enlever la catégorie A de la variable cible. "
            "Sur ce projet, la classe A et B sont les classes très majoritaires et pour répondre à notre besoin, nous faisons ce choix.")

st.code("""#Garder que les variables qui nous intéressent
df[['STATE', 'LONGITUDE', 'OWNER_DESCR', 'REGION',
        'Climat', 'CAUSES_GROUP', 'LATITUDE', 'Type_1', 'SIZE_ENCODED']]"""
, line_numbers=True)

#2e paragraphe : Train/Test/Split
st.header("2- Train/Test/Split")
st.code("""#Séparation de la variable cible
data = df.drop(columns = ['FIRE_SIZE', 'FIRE_SIZE_CLASS', 'DISCOVERY_DATE', 'DISCOVERY_TIME', 'STAT_CAUSE_DESCR', 'SIZE_ENCODED', 'OBJECTID'])
target = df['SIZE_ENCODED']

#Séparation test à 20%
X_train, X_test, y_train, y_test = train_test_split(data, target, random_state = 42, test_size = 0.2)

# Important : réaligner les index
y_train = y_train.set_axis(X_train.index)
y_test = y_test.set_axis(X_test.index)

#Séparation des variables catégorielles et numériques 
num_train = X_train.select_dtypes(include = 'number')
num_test = X_test.select_dtypes(include = 'number')
cat_train = X_train.select_dtypes(exclude = 'number')
cat_test = X_test.select_dtypes(exclude = 'number')""", line_numbers=True)

#3e paragraphe : 
st.header("3- Imputation valeurs manquantes")

st.code("""#Valeurs manquantes
#variables numériques - Choix d'imputer par la médiane
num_imputer = SimpleImputer(missing_values = np.nan,
                           strategy = 'median')

num_train_imputed = pd.DataFrame(num_imputer.fit_transform(num_train),
                                columns = ['FIRE_YEAR', 'DISCOVERY_DOY', 'LATITUDE',
                                           'LONGITUDE', 'temp_mean_0', 'prcp_sum_0', 'wspd_mean_0', 'temp_mean_10',
                                           'prcp_sum_10', 'wspd_mean_10', 'temp_mean_30', 'prcp_sum_30',
                                           'wspd_mean_20', 'temp_mean_60', 'prcp_sum_60', 'wspd_mean_60',
                                           'temp_mean_180', 'prcp_sum_180', 'wspd_mean_180', 'YEAR', 'MONTH','DAY', 'WEEKDAY'],
                                index = num_train.index)

num_test_imputed = pd.DataFrame(num_imputer.transform(num_test),
                                columns = ['FIRE_YEAR', 'DISCOVERY_DOY', 'LATITUDE',
                                           'LONGITUDE', 'temp_mean_0', 'prcp_sum_0', 'wspd_mean_0', 'temp_mean_10',
                                           'prcp_sum_10', 'wspd_mean_10', 'temp_mean_30', 'prcp_sum_30',
                                           'wspd_mean_20', 'temp_mean_60', 'prcp_sum_60', 'wspd_mean_60',
                                           'temp_mean_180', 'prcp_sum_180', 'wspd_mean_180', 'YEAR', 'MONTH','DAY', 'WEEKDAY'],
                                index = num_test.index)

""", line_numbers=True)



# #4e paragraphe : Encodage variable cible
st.header("4- Encodage variable cible")
st.code("""#Encodage variable cible
codage = {'small': 0, 'medium': 1, 'very_large': 2}

y_train_encoded = y_train.map(codage)
y_test_encoded = y_test.map(codage)
""", line_numbers=True)

# #5e paragraphe : Encodage variables catégorielles
st.header("5- Encodage variables catégorielles")
st.code("""
#Variables catégorielles ordinales
# Colonnes ordinales
ordinal_cols = ['SAISON', 'PERIODE_DAY', 'DAY_NAME']

# Ordre défini
saison_order = ['Hiver', 'Printemps', 'Été', 'Automne']
periode_order = ['Matin Tôt', 'Matinée', 'Après-Midi', 'Soirée', 'Nuit']
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Instanciation de l'encodeur
ord_enc = OrdinalEncoder(categories=[saison_order, periode_order, day_order])

# Fit sur le train
ord_enc.fit(cat_train[ordinal_cols])

# Transformation
ord_train = pd.DataFrame(
    ord_enc.transform(cat_train[ordinal_cols]),
    columns=ordinal_cols,
    index=cat_train.index
)

ord_test = pd.DataFrame(
    ord_enc.transform(cat_test[ordinal_cols]),
    columns=ordinal_cols,
    index=cat_test.index
)

#Variables catégorielles nominales
from category_encoders import TargetEncoder
# Séparation des colonnes
target_encode_cols = ['STATE', 'REGION', 'OWNER_DESCR', 'Type_1', 'Climat']

# Instanciation de TargetEncoder
target_encoder = TargetEncoder()

# On entraîne le modèle sur le jeu d'entraînement
target_encoder.fit(cat_train[target_encode_cols], y_train_encoded)

# On applique sur train & test
target_train = pd.DataFrame(target_encoder.transform(cat_train[target_encode_cols]),
                            columns = target_encode_cols,
                            index = cat_train.index)

target_test = pd.DataFrame(target_encoder.transform(cat_test[target_encode_cols]),
                           columns = target_encode_cols,
                           index = cat_test.index)
                           
#Variable catégorielle nominale (peu de modalités)                            
from sklearn.preprocessing import OneHotEncoder

ohe = OneHotEncoder(sparse_output=False, drop='first')

ohe.fit(cat_train[['CAUSES_GROUP']])

# On applique sur train & test
ohe_train = pd.DataFrame(ohe.transform(cat_train[['CAUSES_GROUP']]),
                            columns = ohe.get_feature_names_out(['CAUSES_GROUP']),
                            index = cat_train.index)

ohe_test = pd.DataFrame(ohe.transform(cat_test[['CAUSES_GROUP']]),
                           columns = ohe.get_feature_names_out(['CAUSES_GROUP']),
                           index = cat_test.index)

#df variables catégorielles
cat_train_encoded = pd.concat([ord_train, target_train, ohe_train], axis=1)
cat_test_encoded = pd.concat([ord_test, target_test, ohe_test], axis=1)

#concatenation
X_train_arbre = pd.concat([num_train_imputed, cat_train_encoded], axis = 1)
X_test_arbre = pd.concat([num_test_imputed, cat_test_encoded], axis = 1)
""", line_numbers=True)


# #6e paragraphe : Modèle Random Forest
st.header("6- Modèle & Hyperparamètres")
st.markdown("Après un premier test et une recherche d'hyperparamètres, nous obtenons : ")
st.markdown("#### **La recherche d'hyperparamètres :**")
st.code("""from sklearn.model_selection import GridSearchCV

clf_rf = RandomForestClassifier(criterion = 'gini', random_state=42)

param_grid_rf = {'n_estimators': [100, 150],
                 'max_depth': [10, 15, 20],
                 'min_samples_split': [5, 8, 10],
                 'min_samples_leaf': [1, 5, 10],
                 'max_features': ['sqrt'],
                 'class_weight': ['balanced', {0:1, 1:3, 2:10}]
}

clf_rf_final = GridSearchCV(
    estimator=clf_rf,                  
    param_grid=param_grid_rf,          
    cv=3,                              
    scoring='f1_macro',             
    n_jobs=-1,
    refit=True,
    return_train_score=True
)

clf_rf_final.fit(X_train_arbre, y_train_encoded)
print(clf_rf_final.best_params_)
""", line_numbers=True)

st.markdown("#### **Et le modèle :**")
st.code("""#Instanciation du modèle
rf2 = RandomForestClassifier(max_depth= 20, 
                            max_features =  'sqrt', 
                            min_samples_split= 5,
                            min_samples_leaf=10,
                            n_estimators= 150,
                            class_weight={0:1, 1:3, 2:10},
                            criterion = 'gini', 
                            random_state=42,
                            ccp_alpha=0.001
                            )

#Entraînement du modèle
rf2.fit(X_train_arbre, y_train_encoded)

print("Score sur ensemble Train : ", rf2.score(X_train_arbre, y_train_encoded))
print("Score sur ensemble Test : ", rf2.score(X_test_arbre, y_test_encoded))

# Évaluation du modèle
from sklearn.metrics import classification_report

y_pred_rf2= rf2.predict(X_test_arbre)
display(pd.crosstab(y_test_encoded, y_pred_rf2, rownames = ['Classes réelles'], colnames = ['Classes prédites']))

print(classification_report(y_test_encoded, y_pred_rf2))

#Importances de chaques variables explicatives

feat_importances_arbre = pd.DataFrame(rf2.feature_importances_,
                                      index = X_test_arbre.columns,
                                      columns = ['Importances'])

feat_importances_arbre.sort_values(by = 'Importances', ascending = False, inplace = True)

feat_importances_arbre.plot(kind = 'bar', figsize = (10,8))
""", line_numbers=True)

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
st.header("7- Modèle avec 8 variables")

st.markdown("Nous gardons les 8 variables les plus importantes après la création du premier modèle.")
st.markdown("#### **Modèle final :**")
st.code("""
        
X_train_arbre8 = X_train_arbre[['STATE', 'LONGITUDE', 'OWNER_DESCR', 'REGION', 'Climat', 'LATITUDE', 'CAUSES_GROUP_Naturel', 'Type_1']]
X_test_arbre8 = X_test_arbre[['STATE', 'LONGITUDE', 'OWNER_DESCR', 'REGION', 'Climat', 'LATITUDE', 'CAUSES_GROUP_Naturel', 'Type_1']]

#Instanciation du modèle
rf_bi = RandomForestClassifier(max_depth= 20, 
                            max_features =  'sqrt', 
                            min_samples_split= 5,
                            min_samples_leaf=10,
                            n_estimators= 150,
                            class_weight={0:1, 1:3, 2:10},
                            criterion = 'gini', 
                            random_state=42,
                            ccp_alpha=0.001
                            )

#Entraînement du modèle
rf_bi.fit(X_train_arbre8, y_train_encoded)
""" )

#Résultats
st.write("**Score sur ensemble Train :**  0.642138105003806 \n\n"
"**Score sur ensemble Test :**  0.6421793820634417")

st.code("""
# Évaluation du modèle

y_pred_clf_bi= rf_bi.predict(X_test_arbre8)
display(pd.crosstab(y_test_encoded, y_pred_clf_bi, rownames = ['Classes réelles'], colnames = ['Classes prédites']))

print(classification_report(y_test_encoded, y_pred_clf_bi))
""")

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

df_report = pd.DataFrame(report_data2, index=index_labels)


# Charger l'image depuis le disque
image2 = Image.open("/Users/mallou/Documents/Projet Data/Feux_USA/PDF/output2.png")

# Afficher l'image
st.write("### Importance des variables")
st.image(image2, use_container_width=True)












# Contenu dans la barre côté gauche
st.sidebar.markdown("# Présentation du modèle de prédiction")
st.sidebar.markdown("---")