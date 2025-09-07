import streamlit as st
import pandas as pd
import joblib
import folium
from streamlit_folium import st_folium
import download_datasets

#streamlit run streamlit_app.py



# -------------------------------
# Chargement du pipeline
# -------------------------------
pipeline = joblib.load("/Users/mallou/Documents/Projet Data/Streamlit_fires/Streamlit/pipeline_model.pkl")
st.title("Prédiction de la classe d'un feu")

# -------------------------------
# Dictionnaire des coordonnées par État
# -------------------------------
state_coords = {
    'CA': [
        (40.96805556, -122.43388889),
        (41.23361111, -122.28333333),
        (38.43333333, -120.51),
        (38.52333333, -120.21166667),
        (38.78, -120.26),
        (34.15388889, -117.84111111),
        (33.71888889, -117.43361111),
        (38.83972222, -119.88638889),
        (34.74833333, -119.41027778),
        (38.29444444, -119.54)
    ],
    'NM': [
        (33.54527778, -105.22944444),
        (33.31583333, -105.51222222),
        (33.44444444, -105.63111111),
        (32.46722222, -104.94166667),
        (36.69166667, -107.38583333),
        (36.93472222, -107.34972222),
        (36.65944444, -107.19638889),
        (36.64583333, -107.22694444),
        (35.70111111, -105.70916667),
        (36.92277778, -107.23638889)
    ],
    'NC': [
        (35.22833333, -82.88444444),
        (35.00027778, -83.35111111),
        (36.00166667, -81.59),
        (35.985, -81.85166667),
        (35.9, -81.68333333),
        (36.035, -81.585),
        (35.00138889, -83.38416667),
        (35.33638889, -83.89722222),
        (35.28, -83.87611111),
        (35.42194444, -83.42194444)
    ],
    'OR': [
        (44.91111111, -119.69611111),
        (42.51472222, -121.12),
        (42.13694444, -120.70166667),
        (43.99138889, -118.73277778),
        (42.58694444, -121.18638889),
        (42.53222222, -121.12055556),
        (43.52638889, -121.94611111),
        (44.23666667, -118.87333333),
        (44.46388889, -118.54722222),
        (44.53472222, -118.63166667)
    ],
    'CO': [
        (39.29222222, -105.18305556),
        (37.345, -102.80583333),
        (38.89111111, -105.43194444),
        (39.41277778, -105.14111111),
        (39.33805556, -105.17416667),
        (39.2975, -105.05972222),
        (39.34166667, -105.32138889),
        (39.48055556, -105.13666667),
        (39.3525, -105.15555556),
        (39.38333333, -105.29333333)
    ],
    'WA': [
        (46.22083333, -117.785),
        (45.715, -121.34833333),
        (45.66416667, -121.01083333),
        (45.66222222, -120.91583333),
        (45.78694444, -121.40083333),
        (45.63305556, -121.11138889),
        (45.7, -121.72388889),
        (48.70666667, -117.09833333),
        (48.82333333, -117.05444444),
        (47.39527778, -121.56055556)
    ],
    'MT': [
        (48.92194444, -115.0925),
        (48.99833333, -115.16555556),
        (47.66555556, -115.56916667),
        (48.89944444, -115.10694444),
        (48.96666667, -115.20666667),
        (48.89444444, -115.16527778),
        (48.22805556, -115.48027778),
        (48.76666667, -114.87833333),
        (48.53888889, -115.93472222),
        (48.84694444, -115.66222222)
    ],
    'AZ': [
        (35.23638889, -112.21638889),
        (32.68555556, -109.86916667),
        (33.71611111, -111.21777778),
        (33.95972222, -111.39805556),
        (33.72333333, -111.275),
        (33.83972222, -109.115),
        (34.40527778, -111.0275),
        (34.54166667, -110.9025),
        (34.53055556, -111.01277778),
        (34.45555556, -110.75805556)
    ],
    'NV': [
        (38.25555556, -118.48611111),
        (39.11666667, -119.845),
        (38.60222222, -119.42972222),
        (39.08555556, -119.87416667),
        (39.47972222, -119.85138889),
        (39.11055556, -119.85972222),
        (38.98916667, -119.84638889),
        (36.25527778, -115.82555556),
        (39.0, -119.87166667),
        (36.13583333, -115.69666667)
    ],
    'SD': [
        (43.065, -103.66055556),
        (43.89916667, -102.95472222),
        (43.89277778, -102.94805556),
        (43.66194444, -102.83444444),
        (43.72666667, -102.76277778),
        (43.77444444, -103.66722222),
        (43.59916667, -103.70916667),
        (43.61638889, -103.65555556),
        (43.59361111, -103.6225),
        (44.07888889, -103.61138889)
    ],
    'MN': [
        (47.54138889, -94.57361111),
        (47.59888889, -94.53916667),
        (47.5625, -94.64833333),
        (47.3175, -93.93388889),
        (47.35444444, -94.17194444),
        (47.35444444, -94.17222222),
        (47.25305556, -93.91027778),
        (47.48166667, -93.67138889),
        (47.40888889, -94.07305556),
        (47.11333333, -94.54277778)
    ],
    'TX': [
        (33.78611111, -96.15),
        (31.3125, -94.27083333),
        (33.34583333, -97.59583333),
        (31.38666667, -95.15055556),
        (31.35416667, -95.08527778),
        (31.15444444, -93.62388889),
        (31.15888889, -93.62083333),
        (31.15972222, -93.61888889),
        (31.14583333, -93.61527778),
        (31.16416667, -93.61527778)
    ],
    'AR': [
        (34.89055556, -92.89138889),
        (36.12888889, -92.3575),
        (35.96888889, -92.38944444),
        (35.24944444, -93.68555556),
        (34.89833333, -93.40527778),
        (34.68722222, -93.82361111),
        (34.70277778, -93.81388889),
        (34.42277778, -94.1325),
        (35.68555556, -94.01861111),
        (35.96694444, -92.23388889)
    ],
    'SC': [
        (34.41805556, -81.50916667),
        (33.09888889, -79.77083333),
        (32.94444444, -79.67972222),
        (32.94222222, -79.69388889),
        (33.04666667, -79.70138889),
        (33.20777778, -79.57916667),
        (32.95972222, -79.79555556),
        (33.30027778, -79.81638889),
        (34.40166667, -81.57111111),
        (34.67611111, -81.63222222)
    ],
    'WY': [
        (44.07583333, -107.30305556),
        (44.45861111, -109.74138889),
        (44.93416667, -107.85027778),
        (44.89888889, -107.50333333),
        (44.37194444, -104.17416667),
        (41.48444444, -106.60361111),
        (41.31027778, -107.175),
        (42.59722222, -108.82472222),
        (43.33916667, -111.00305556),
        (43.16527778, -110.17361111)
    ],
    'LA': [
        (30.95388889, -93.07166667),
        (31.44472222, -93.1225),
        (31.20277778, -92.66194444),
        (30.92805556, -93.12805556),
        (31.24027778, -92.61305556),
        (31.05833333, -92.95),
        (31.55277778, -92.59833333),
        (31.26027778, -92.75555556),
        (31.5075, -93.23222222),
        (31.39194444, -93.13611111)
    ],
    'OK': [
        (35.59583333, -100.01305556),
        (36.97805556, -102.58305556),
        (34.80805556, -94.51777778),
        (34.74638889, -94.51666667),
        (34.70527778, -94.50222222),
        (34.76222222, -94.48638889),
        (34.73444444, -94.54611111),
        (34.36805556, -94.73361111),
        (34.21333333, -94.74027778),
        (34.65138889, -94.64861111)
    ],
    'UT': [
        (39.99055556, -111.37722222),
        (39.93805556, -111.39555556),
        (39.48, -111.82611111),
        (39.51055556, -111.83666667),
        (37.77666667, -109.85083333),
        (40.015, -111.23833333),
        (40.14944444, -111.41444444),
        (40.11583333, -111.32638889),
        (40.07888889, -111.37305556),
        (37.99027778, -112.325)
    ],
    'FL': [
        (30.2, -84.38333333),
        (29.0925, -81.89111111),
        (29.16805556, -81.89611111),
        (29.2025, -81.90194444),
        (29.21, -81.90527778),
        (30.30138889, -84.66888889),
        (29.42805556, -81.72972222),
        (29.03333333, -81.42083333),
        (29.04555556, -81.61722222),
        (30.34027778, -84.26861111)
    ],
    'ID': [
        (48.99, -116.30138889),
        (48.41833333, -117.00083333),
        (48.19861111, -116.10222222),
        (48.12916667, -116.28666667),
        (48.26527778, -116.09305556),
        (48.79972222, -116.465),
        (48.25055556, -116.06277778),
        (48.37555556, -116.22666667),
        (43.53583333, -115.27055556),
        (43.60111111, -115.93)
    ],
    'KS': [
        (37.08805556, -101.63694444),
        (37.06833333, -101.99944444),
        (37.15777778, -101.78972222),
        (37.02472222, -101.99333333),
        (37.34444444, -101.70944444),
        (37.07388889, -101.70972222),
        (37.09027778, -101.75555556),
        (37.0975, -101.77722222),
        (37.045, -101.79),
        (37.10222222, -101.69611111)
    ],
    'MO': [
        (37.65, -90.80083333),
        (37.82166667, -91.23861111),
        (37.77916667, -91.01),
        (37.82333333, -90.93333333),
        (37.78583333, -91.05055556),
        (37.80833333, -91.05833333),
        (37.76277778, -91.1325),
        (37.81111111, -91.06722222),
        (37.89861111, -90.98722222),
        (37.72083333, -90.97222222)
    ],
    'NE': [
        (42.98361111, -104.02555556),
        (42.775, -101.09416667),
        (42.73305556, -100.91),
        (41.80611111, -100.42527778),
        (42.5875, -103.35166667),
        (42.92611111, -103.585),
        (42.79166667, -102.97972222),
        (41.83777778, -100.29194444),
        (42.755, -102.98583333),
        (42.70055556, -103.61083333)
    ],
    'MI': [
        (43.57111111, -85.97916667),
        (43.94416667, -82.99027778),
        (43.43, -85.80666667),
        (43.45361111, -85.7925),
        (43.51861111, -85.63527778),
        (43.815, -85.91333333),
        (43.61833333, -85.69277778),
        (44.215, -85.71916667),
        (43.63277778, -85.77194444),
        (43.62083333, -85.78416667)
    ],
    'KY': [
        (36.625, -84.20194444),
        (36.84666667, -84.27027778),
        (37.53833333, -84.03305556),
        (36.62277778, -84.50305556),
        (36.77333333, -84.58111111),
        (37.06166667, -83.4975),
        (36.73055556, -84.44722222),
        (36.675, -84.44),
        (36.78, -84.38444444),
        (36.715, -84.44666667)
    ],
    'OH': [
        (38.70666667, -82.66972222),
        (39.37388889, -82.12722222),
        (39.50944444, -81.25722222),
        (39.49416667, -82.28166667),
        (39.32638889, -81.995),
        (38.56194444, -82.70611111),
        (39.46944444, -82.18666667),
        (38.55, -82.63222222),
        (39.48194444, -82.28638889),
        (38.83277778, -82.58888889)
    ],
    'IN': [
        (39.03166667, -86.175),
        (39.08888889, -86.35833333),
        (38.99416667, -86.36944444),
        (38.05, -86.66666667),
        (38.60472222, -86.68611111),
        (39.01666667, -86.45527778),
        (39.06277778, -86.14666667),
        (38.74888889, -86.54638889),
        (38.59472222, -86.65472222),
        (38.89083333, -86.49972222)
    ],
    'VA': [
        (38.55777778, -79.07166667),
        (38.3, -79.38333333),
        (38.74138889, -79.02944444),
        (37.76027778, -80.20194444),
        (37.64583333, -80.15027778),
        (37.83194444, -80.09388889),
        (37.8975, -79.57611111),
        (38.18194444, -79.84444444),
        (36.79694444, -82.80833333),
        (38.85, -78.35305556)
    ],
    'IL': [
        (37.50305556, -89.41777778),
        (37.395, -88.675),
        (37.56111111, -88.65305556),
        (37.67472222, -88.4125),
        (37.2625, -89.46277778),
        (37.5925, -89.46166667),
        (37.49166667, -88.68222222),
        (37.61055556, -89.25916667),
        (37.63944444, -89.41555556),
        (37.57055556, -89.50277778)
    ],
    'TN': [
        (36.46638889, -82.01),
        (35.09305556, -84.38111111),
        (35.19027778, -84.33333333),
        (35.18583333, -84.29611111),
        (35.19138889, -84.33861111),
        (35.05638889, -84.36888889),
        (35.04027778, -84.37361111),
        (36.55194444, -81.96888889),
        (35.215, -84.46527778),
        (35.16361111, -84.40138889)
    ],
    'GA': [
        (34.89444444, -84.66694444),
        (34.59722222, -85.02083333),
        (34.74555556, -85.04472222),
        (34.87194444, -83.93416667),
        (33.59638889, -83.33583333),
        (33.21361111, -83.48444444),
        (33.3275, -83.43666667),
        (34.69555556, -83.39416667),
        (34.89055556, -84.01722222),
        (34.80944444, -83.3175)
    ],
    'AK': [
        (60.05333333, -149.44),
        (60.50611111, -145.34388889),
        (60.885, -149.045),
        (59.08722222, -135.44138889),
        (55.58333333, -133.03333333),
        (55.46916667, -131.82138889),
        (55.94972222, -132.94888889),
        (58.62944444, -134.93944444)
    ],
    'ND': [
        (46.45, -97.39444444),
        (47.28194444, -103.48333333),
        (47.27777778, -103.48888889),
        (47.27777778, -103.48194444),
        (46.86861111, -103.69694444),
        (46.90277778, -103.54583333),
        (47.59805556, -103.6375),
        (46.80055556, -103.45055556),
        (46.65277778, -103.32444444),
        (46.52, -103.79861111)
    ],
    'WV': [
        (38.34166667, -79.9625),
        (38.8, -80.25111111),
        (38.97722222, -79.59083333),
        (38.625, -79.21666667),
        (38.72916667, -79.465),
        (38.49888889, -79.63861111),
        (38.35611111, -80.58361111),
        (38.76722222, -79.3225),
        (39.26666667, -80.625),
        (37.97194444, -80.13472222)
    ],
    'WI': [
        (46.02444444, -88.83694444),
        (45.17166667, -88.46361111),
        (46.16111111, -90.91916667),
        (46.02333333, -88.83666667),
        (45.54527778, -88.71666667),
        (45.97416667, -90.05138889),
        (46.33916667, -90.92972222),
        (45.41694444, -88.76638889),
        (45.32194444, -88.59305556),
        (45.29944444, -88.53694444)
    ],
    'NH': [
        (44.08333333, -71.45),
        (44.71666667, -71.28333333),
        (44.41138889, -71.51138889),
        (44.005, -71.90833333),
        (43.80277778, -71.83583333),
        (43.98333333, -71.35),
        (44.12166667, -71.28833333),
        (43.75, -72.12166667),
        (43.83333333, -71.48333333),
        (44.03333333, -71.36666667)
    ],
    'PA': [
        (41.41555556, -78.90722222),
        (41.86472222, -78.66694444),
        (41.73833333, -79.08111111),
        (41.785, -76.11277778),
        (41.7675, -79.10277778),
        (41.82388889, -79.12194444),
        (41.86638889, -78.70444444),
        (41.85083333, -78.97611111),
        (41.69222222, -78.81972222),
        (41.775, -79.22694444)
    ],
    'AL': [
        (33.34861111, -86.09944444),
        (33.385, -85.96777778),
        (32.90416667, -87.33055556),
        (33.6025, -85.67472222),
        (32.7825, -87.17444444),
        (34.24527778, -87.26638889),
        (31.09722222, -86.48333333),
        (32.9175, -87.49722222),
        (31.11472222, -86.77138889),
        (33.66722222, -85.62583333)
    ],
    'MS': [
        (31.06833333, -89.09916667),
        (31.17805556, -89.08611111),
        (30.55888889, -89.075),
        (30.55916667, -89.06194444),
        (31.06611111, -89.02888889),
        (30.68666667, -88.86833333),
        (31.08666667, -89.12166667),
        (31.01138889, -89.12638889),
        (30.96305556, -88.91027778),
        (30.96277778, -88.92555556)
    ],
    'ME': [
        (44.36805556, -70.8125),
        (44.325, -70.81333333),
        (44.31666667, -70.81666667),
        (44.31666667, -70.85),
        (45.2001, -68.0661),
        (45.1834, -68.1995),
        (45.1834, -68.0495),
        (45.1834, -68.1161),
        (44.9667, -67.0661)
    ],
    'VT': [
        (43.93722222, -72.89444444),
        (43.88916667, -73.06333333),
        (43.67111111, -72.92111111),
        (43.25333333, -72.53666667),
        (43.38444444, -72.93),
        (43.335, -72.905),
        (43.91666667, -73.11666667),
        (44.9, -73.11666667),
        (43.28833333, -73.05833333),
        (43.8, -72.83333333)
    ],
    'NY': [
        (42.53333333, -76.73333333),
        (42.58833333, -76.82166667),
        (42.56111111, -76.7825),
        (41.60302, -73.61257),
        (41.57404, -73.67433),
        (41.57348, -73.67379),
        (41.57348, -73.67374),
        (41.57343, -73.67373),
        (41.76349, -73.89488),
        (40.69, -72.99)
    ],
    'IA': [
        (42.1167, -96.367),
        (42.0, -92.6669),
        (41.9833, -92.6335),
        (41.975, -92.6335),
        (41.9744, -92.6391),
        (41.9778, -92.6391),
        (41.9567, -92.6346),
        (41.9605, -92.636),
        (41.9608, -92.6363),
        (41.9575, -92.6346)
    ],
    'DC': [
        (38.94837, -77.00484),
        (38.93587, -76.98837),
        (38.9333, -77.05),
        (38.9333, -77.05),
        (38.93851, -77.04961),
        (38.94312, -77.05097),
        (38.95762, -77.05395),
        (38.91653, -77.08213),
        (38.94787, -77.04983),
        (38.94847, -77.0041)
    ],
    'MD': [
        (39.4731, -77.75192),
        (39.47381, -77.75356),
        (39.45497, -77.72821),
        (39.475, -77.75167),
        (39.50157, -77.840549),
        (39.37437, -77.740816),
        (38.97155, -77.160842),
        (38.9927, -77.237135),
        (39.36446, -77.739106),
        (39.00043, -76.867484)
    ],
    'CT': [
        (41.9233, -73.35331),
        (41.28777778, -72.46777778),
        (41.5573768, -72.3442483),
        (41.4766614, -72.3921201),
        (41.5677366, -72.5095441),
        (41.983993, -72.5555531)
    ],
    'MA': [
        (42.026867, -70.086019),
        (41.931753, -70.052903),
        (41.969394, -70.070606),
        (41.9048, -69.9789),
        (42.064, -70.1717),
        (41.9579, -70.0322),
        (42.0404, -70.2086),
        (41.9959, -70.0189)
    ],
    'NJ': [
        (40.4333, -73.9833),
        (41.133396, -74.883),
        (40.966796, -75.116),
        (41.166795, -74.883),
        (41.141796, -74.859),
        (40.968696, -75.115),
        (41.125095, -74.945),
        (41.266794, -74.837),
        (40.995895, -75.12),
        (41.120896, -74.933)
    ],
    'HI': [
        (20.7617, -156.2453),
        (20.7922, -156.2678),
        (20.6667, -156.1167),
        (19.3833, -155.1333),
        (19.29518, -155.11327),
        (19.324, -155.04632),
        (19.3333, -155.0333)
    ],
    'DE': [
        (39.25, -75.41666667),
        (38.78333333, -75.2),
        (38.8297, -75.2342),
        (39.2, -75.42083),
        (38.8131, -75.2),
        (38.82528, -75.22278)
    ],
    'PR': [
        (18.0, -67.1),
        (18.01666667, -67.1),
        (18.38333333, -67.48333333),
        (18.01666667, -67.1)
    ],
    'RI': [
        (41.61892, -71.49163),
        (41.55533, -71.46497),
        (41.68775, -71.56579),
        (41.40327, -71.56268),
        (41.36382, -71.68172),
        (41.69245, -71.54321),
        (41.41909, -71.65458),
        (41.47744, -71.76515),
        (41.66873, -71.56982),
        (41.4546, -71.64574)
    ]
}

# -------------------------------
# Dictionnaire des infos par État
# -------------------------------
state_info = {
    'AK': {'Type_1': 'Toundra', 'Climat': 'Arctique à continental'},
    'AL': {'Type_1': 'Forêt', 'Climat': 'Subtropical humide'},
    'AR': {'Type_1': 'Forêt', 'Climat': 'Subtropical humide'},
    'AZ': {'Type_1': 'Désert', 'Climat': 'Aride à semi-aride'},
    'CA': {'Type_1': 'Désert', 'Climat': 'Méditerranéen à désertique'},
    'CO': {'Type_1': 'Montagne', 'Climat': 'Continental sec'},
    'CT': {'Type_1': 'Forêt', 'Climat': 'Continental humide'},
    'DC': {'Type_1': 'Forêt', 'Climat': 'Subtropical humide'},
    'DE': {'Type_1': 'Forêt', 'Climat': 'Subtropical humide'},
    'FL': {'Type_1': 'Côtier', 'Climat': 'Tropical à subtropical'},
    'GA': {'Type_1': 'Forêt', 'Climat': 'Subtropical humide'},
    'HI': {'Type_1': 'Côtier', 'Climat': 'Tropical'},
    'IA': {'Type_1': 'Prairie', 'Climat': 'Continental humide'},
    'ID': {'Type_1': 'Montagne', 'Climat': 'Continental sec'},
    'IL': {'Type_1': 'Prairie', 'Climat': 'Continental humide'},
    'IN': {'Type_1': 'Prairie', 'Climat': 'Continental humide'},
    'KS': {'Type_1': 'Prairie', 'Climat': 'Continental semi-aride'},
    'KY': {'Type_1': 'Forêt', 'Climat': 'Subtropical humide'},
    'LA': {'Type_1': 'Forêt', 'Climat': 'Subtropical humide'},
    'MA': {'Type_1': 'Forêt', 'Climat': 'Continental humide'},
    'MD': {'Type_1': 'Forêt', 'Climat': 'Subtropical humide'},
    'ME': {'Type_1': 'Forêt', 'Climat': 'Continental humide'},
    'MI': {'Type_1': 'Forêt', 'Climat': 'Continental humide'},
    'MN': {'Type_1': 'Forêt', 'Climat': 'Continental humide'},
    'MO': {'Type_1': 'Prairie', 'Climat': 'Continental humide'},
    'MS': {'Type_1': 'Forêt', 'Climat': 'Subtropical humide'},
    'MT': {'Type_1': 'Montagne', 'Climat': 'Continental sec'},
    'NC': {'Type_1': 'Forêt', 'Climat': 'Subtropical humide'},
    'ND': {'Type_1': 'Prairie', 'Climat': 'Continental semi-aride'},
    'NE': {'Type_1': 'Prairie', 'Climat': 'Continental semi-aride'},
    'NH': {'Type_1': 'Forêt', 'Climat': 'Continental humide'},
    'NJ': {'Type_1': 'Forêt', 'Climat': 'Subtropical humide'},
    'NM': {'Type_1': 'Désert', 'Climat': 'Aride à semi-aride'},
    'NV': {'Type_1': 'Désert', 'Climat': 'Aride'},
    'NY': {'Type_1': 'Forêt', 'Climat': 'Continental humide'},
    'OH': {'Type_1': 'Forêt', 'Climat': 'Continental humide'},
    'OK': {'Type_1': 'Prairie', 'Climat': 'Continental semi-aride'},
    'OR': {'Type_1': 'Forêt', 'Climat': 'Océanique'},
    'PA': {'Type_1': 'Forêt', 'Climat': 'Continental humide'},
    'PR': {'Type_1': 'Côtier', 'Climat': 'Tropical humide'},
    'RI': {'Type_1': 'Forêt', 'Climat': 'Continental humide'},
    'SC': {'Type_1': 'Forêt', 'Climat': 'Subtropical humide'},
    'SD': {'Type_1': 'Prairie', 'Climat': 'Continental semi-aride'},
    'TN': {'Type_1': 'Forêt', 'Climat': 'Subtropical humide'},
    'TX': {'Type_1': 'Prairie', 'Climat': 'Continental à tropical'},
    'UT': {'Type_1': 'Désert', 'Climat': 'Aride à semi-aride'},
    'VA': {'Type_1': 'Forêt', 'Climat': 'Subtropical humide'},
    'VT': {'Type_1': 'Forêt', 'Climat': 'Continental humide'},
    'WA': {'Type_1': 'Forêt', 'Climat': 'Océanique'},
    'WI': {'Type_1': 'Forêt', 'Climat': 'Continental humide'},
    'WV': {'Type_1': 'Forêt', 'Climat': 'Continental humide'},
    'WY': {'Type_1': 'Prairie', 'Climat': 'Continental sec'}
}

# -------------------------------
# Dictionnaire des propriétaires par État
# -------------------------------
owner_options_by_state = {
    'AK': ['BIA', 'BLM', 'BOR', 'COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'USFS'],
    'AL': ['FWS', 'MISSING/NOT SPECIFIED', 'NPS', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'USFS'],
    'AR': ['BIA', 'COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'UNDEFINED FEDERAL', 'USFS'],
    'AZ': ['BIA', 'BLM', 'BOR', 'FOREIGN', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'UNDEFINED FEDERAL', 'USFS'],
    'CA': ['BIA', 'BLM', 'BOR', 'COUNTY', 'FOREIGN', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'UNDEFINED FEDERAL', 'USFS'],
    'CO': ['BIA', 'BLM', 'BOR', 'COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'UNDEFINED FEDERAL', 'USFS'],
    'CT': ['FWS', 'MISSING/NOT SPECIFIED', 'NPS'],
    'DC': ['NPS'],
    'DE': ['FWS', 'MISSING/NOT SPECIFIED', 'PRIVATE', 'STATE'],
    'FL': ['BIA', 'BOR', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'UNDEFINED FEDERAL', 'USFS'],
    'GA': ['FWS', 'MISSING/NOT SPECIFIED', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'UNDEFINED FEDERAL', 'USFS'],
    'HI': ['COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'NPS', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'UNDEFINED FEDERAL'],
    'IA': ['BIA', 'COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'PRIVATE', 'STATE', 'TRIBAL'],
    'ID': ['BIA', 'BLM', 'BOR', 'COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'UNDEFINED FEDERAL', 'USFS'],
    'IL': ['COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'UNDEFINED FEDERAL', 'USFS'],
    'IN': ['FWS', 'MISSING/NOT SPECIFIED', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'USFS'],
    'KS': ['BIA', 'BLM', 'COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'USFS'],
    'KY': ['MISSING/NOT SPECIFIED', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'UNDEFINED FEDERAL', 'USFS'],
    'LA': ['COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'UNDEFINED FEDERAL', 'USFS'],
    'MA': ['COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE'],
    'MD': ['BLM', 'COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'UNDEFINED FEDERAL'],
    'ME': ['BIA', 'FWS', 'MISSING/NOT SPECIFIED', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'USFS'],
    'MI': ['BIA', 'COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'UNDEFINED FEDERAL', 'USFS'],
    'MN': ['BIA', 'BLM', 'COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'UNDEFINED FEDERAL', 'USFS'],
    'MO': ['FWS', 'MISSING/NOT SPECIFIED', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'USFS'],
    'MS': ['BIA', 'FWS', 'MISSING/NOT SPECIFIED', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'UNDEFINED FEDERAL', 'USFS'],
    'MT': ['BIA', 'BLM', 'COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'UNDEFINED FEDERAL', 'USFS'],
    'NC': ['BIA', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'UNDEFINED FEDERAL', 'USFS'],
    'ND': ['BIA', 'BLM', 'COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'UNDEFINED FEDERAL', 'USFS'],
    'NE': ['BIA', 'FWS', 'MISSING/NOT SPECIFIED', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'USFS'],
    'NH': ['FWS', 'MISSING/NOT SPECIFIED', 'NPS', 'PRIVATE', 'STATE OR PRIVATE', 'USFS'],
    'NJ': ['FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'UNDEFINED FEDERAL'],
    'NM': ['BIA', 'BLM', 'BOR', 'FWS', 'MISSING/NOT SPECIFIED', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'UNDEFINED FEDERAL', 'USFS'],
    'NV': ['BIA', 'BLM', 'BOR', 'COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'UNDEFINED FEDERAL', 'USFS'],
    'NY': ['BIA', 'COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'PRIVATE', 'STATE', 'TRIBAL', 'UNDEFINED FEDERAL', 'USFS'],
    'OH': ['FWS', 'MISSING/NOT SPECIFIED', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'UNDEFINED FEDERAL', 'USFS'],
    'OK': ['BIA', 'BLM', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'UNDEFINED FEDERAL', 'USFS'],
    'OR': ['BIA', 'BLM', 'BOR', 'COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'UNDEFINED FEDERAL', 'USFS'],
    'PA': ['BLM', 'COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'USFS'],
    'PR': ['FWS', 'MISSING/NOT SPECIFIED', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE'],
    'RI': ['FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'PRIVATE', 'STATE'],
    'SC': ['FWS', 'MISSING/NOT SPECIFIED', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'UNDEFINED FEDERAL', 'USFS'],
    'SD': ['BIA', 'BLM', 'BOR', 'COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'UNDEFINED FEDERAL', 'USFS'],
    'TN': ['FWS', 'MISSING/NOT SPECIFIED', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'UNDEFINED FEDERAL', 'USFS'],
    'TX': ['BIA', 'BLM', 'FOREIGN', 'FWS', 'MISSING/NOT SPECIFIED', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'USFS'],
    'UT': ['BIA', 'BLM', 'BOR', 'COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'UNDEFINED FEDERAL', 'USFS'],
    'VA': ['FWS', 'MISSING/NOT SPECIFIED', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'USFS'],
    'VT': ['MISSING/NOT SPECIFIED', 'NPS', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'USFS'],
    'WA': ['BIA', 'BLM', 'BOR', 'COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'UNDEFINED FEDERAL', 'USFS'],
    'WI': ['BIA', 'COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'UNDEFINED FEDERAL', 'USFS'],
    'WV': ['FWS', 'MISSING/NOT SPECIFIED', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'UNDEFINED FEDERAL', 'USFS'],
    'WY': ['BIA', 'BLM', 'BOR', 'COUNTY', 'FWS', 'MISSING/NOT SPECIFIED', 'MUNICIPAL/LOCAL', 'NPS', 'OTHER FEDERAL', 'PRIVATE', 'STATE', 'STATE OR PRIVATE', 'TRIBAL', 'UNDEFINED FEDERAL', 'USFS']}

# -------------------------------
# Fonction pour déterminer la REGION
# -------------------------------
def region(Etat):
  if Etat in ['CT', 'ME', 'MA', 'NH', 'RI', 'VT'] :
    return 'NEW_ENGLAND'
  elif Etat in ['NJ', 'NY', 'PA'] :
    return 'MID_ATLANTIC'
  elif Etat in ['IL', 'IN', 'MI', 'OH', 'WI'] :
    return 'EAST_NORTH_CENTRAL'
  elif Etat in ['IA', 'KS', 'MN', 'MO', 'NE', 'ND','SD']:
    return 'WEST_NORTH_CENTRAL'
  elif Etat in ['DE', 'FL', 'GA', 'MD', 'NC',
   'SC', 'VA', 'WV', 'DC', 'VI']:
    return 'SOUTH_ATLANTIC'
  elif Etat in ['AL', 'KY', 'MS', 'TN']:
    return 'SOUTH_EAST_CENTRAL'
  elif Etat in ['AR', 'LA', 'OK', 'TX']:
    return 'WEST_SOUTH_CENTRAL'
  elif Etat in ['AZ', 'CO', 'ID', 'MT', 'NV', 'NM', 'UT', 'WY']:
    return 'MOUNTAIN'
  elif Etat in ['AK', 'CA', 'HI', 'OR', 'WA']:
    return 'PACIFIC'
  elif Etat in ['PR']:
    return 'FREE_TERRITORY'

# Ajout automatique de REGION à chaque état
for Etat in state_info.keys():
    state_info[Etat]['REGION'] = region(Etat)

# Vérification rapide
for Etat, info in state_info.items():
    if 'REGION' not in info:
        print(f"{Etat} n'a pas de REGION !")

# -------------------------------
# Widgets pour les inputs
# -------------------------------
state = st.selectbox("État", list(state_info.keys()))
owner_descr = st.selectbox("Description du propriétaire", [
    'STATE OR PRIVATE', 'MISSING/NOT SPECIFIED', 'USFS', 'OTHER FEDERAL', 'BIA', 'FWS',
    'TRIBAL', 'PRIVATE', 'STATE', 'BLM', 'NPS', 'BOR', 'FOREIGN', 'MUNICIPAL/LOCAL', 'COUNTY', 'UNDEFINED FEDERAL'
])
causes_group = st.selectbox("CAUSES_GROUP", ['Humain', 'Naturel', 'unknown'])

# -------------------------------
# Affichage de la carte et sélection d'un point
# -------------------------------
st.subheader("Sélectionnez un point sur la carte pour cet État")
st.warning("Cliquer 2 fois sur le même endroit pour valider votre point.")

# Coordonnées de base de l'État
coords = state_coords[state]
center_lat = sum(lat for lat, _ in coords) / len(coords)
center_lon = sum(lon for _, lon in coords) / len(coords)

# Initialisation du point utilisateur si non défini
if 'user_point' not in st.session_state:
    st.session_state['user_point'] = {'lat': center_lat, 'lng': center_lon}

# Création de la carte centrée sur l'État
m = folium.Map(location=[center_lat, center_lon], zoom_start=6)

# Affichage du marker rouge au dernier point choisi
folium.CircleMarker(
    location=[st.session_state['user_point']['lat'], st.session_state['user_point']['lng']],
    radius=7,
    color='red',
    fill=True,
    fill_color='red',
    fill_opacity=0.8,
    popup="Point utilisateur"
).add_to(m)

# Affichage de la carte et récupération du clic utilisateur
output = st_folium(m, width=700, height=400, returned_objects=["last_clicked"])

# Mise à jour du point utilisateur si clic
if output['last_clicked']:
    st.session_state['user_point'] = output['last_clicked']

# Coordonnées du point sélectionné
latitude = st.session_state['user_point']['lat']
longitude = st.session_state['user_point']['lng']
st.write(f"Point sélectionné : Latitude = {latitude}, Longitude = {longitude}")

# -------------------------------
# Récupération des autres infos
# -------------------------------
info = state_info[state]
type_1 = info['Type_1']
climat = info['Climat']
region = info['REGION']

# Affichage des métriques

st.metric(label="Type_1", value=type_1, border=True)
st.metric(label="Climat", value=climat, border=True)
st.metric(label="Région", value=region, border=True)
#st.write(f"Type_1 : {type_1}")
#st.write(f"Climat : {climat}")
#st.write(f"Région : {region}")

# -------------------------------
# Préparation du dataframe
# -------------------------------
input_df = pd.DataFrame({
    'STATE': [state],
    'OWNER_DESCR': [owner_descr],
    'REGION': [region],
    'Climat': [climat],
    'Type_1': [type_1],
    'CAUSES_GROUP': [causes_group],
    'LONGITUDE': [longitude],
    'LATITUDE': [latitude]
})

# -------------------------------
# Bouton de prédiction
# -------------------------------
if st.button("Prédire la taille"):
    prediction = pipeline.predict(input_df)[0]
    proba = pipeline.predict_proba(input_df)[0]
    codage_inverse = {0: 'small', 1: 'medium', 2: 'very_large'}
    st.success(f"La prédiction est : {codage_inverse[prediction]}")

    st.subheader("Probabilités par classe")
    for cls, p in zip(['small', 'medium', 'very_large'], proba):
        st.write(f"{cls}: {p:.2f}")
