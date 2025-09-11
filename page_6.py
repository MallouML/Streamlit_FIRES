import streamlit as st
import pandas as pd

#/Users/mallou/Documents/Projet\ Data/Feux_USA/.conda/bin/streamlit run "/Users/mallou/Documents/Projet Data/Feux_USA/Streamlit/streamlit_app.py"

st.header("✅ Conclusion")

st.success("De 1,88 M d’incendies à un **bouclier prédictif** utile au terrain.")

st.markdown("""
### 📊 Ce que nous avons démontré
- Transformer **1,88 M** d’événements en **connaissance actionnable**
- Identifier les **zones & saisons critiques**
- Distinguer les **causes humaines (≈85%)** des causes naturelles
- 🎯 **3 %** des feux concentrent **≈70 %** des dégâts → **prioriser l’exceptionnel**
""")

st.divider()

# Petits indicateurs qui claquent
c1, c2 = st.columns(2)
c1.metric("Volume analysé", "1 880 465", border = True)
c2.metric("Humaine", "≈85 %", border = True)

c3, c4 = st.columns(2)
c3.metric("Pareto", "3 % → 70 %", border = True)
c4.metric("Gain décision", "5–10 min", border = True)

st.divider()

st.markdown("""
### 🌍 Impact opérationnel
- Même imparfait, le prototype **apporte déjà de la valeur**
- Donne **5–10 minutes d’avance** pour décider (aérien/terrestre)
- Ces minutes peuvent **tout changer** entre un feu contenu et une catastrophe
""")

st.markdown("""
### 🔥 Exemple concret
> *Un orage déclenche **10 feux** simultanés.*
> Avec notre outil, les équipes identifient **les 2–3 foyers** à haut risque → moyens envoyés **au bon endroit, au bon moment**.
""")

st.divider()

st.markdown("""
### 🚀 Clôture inspirante
**De l’étincelle à la décision**, la donnée devient un **bouclier prédictif** :
un pas de plus vers une prévention plus intelligente, capable de protéger **nos forêts, nos communautés… et nos vies.**
""")

st.caption("✨ Derrière chaque donnée, il y a une forêt, une famille, et des pompiers en première ligne.")

# Contenu dans la barre côté gauche
st.sidebar.markdown("# Conclusion")
st.sidebar.markdown("---")
