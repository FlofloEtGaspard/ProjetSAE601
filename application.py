"""
📝 **Instructions** :
- Installez toutes les bibliothèques nécessaires en fonction des imports présents dans le code, utilisez la commande suivante :conda create -n projet python pandas numpy ..........
- Complétez les sections en écrivant votre code où c’est indiqué.
- Ajoutez des commentaires clairs pour expliquer vos choix.
- Utilisez des emoji avec windows + ;
- Interprétez les résultats de vos visualisations (quelques phrases).
"""

### 1. Importation des librairies et chargement des données
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

# Chargement des données
df = pd.read_csv("h:\Mes documents\SD3\SAE 601\data\ds_salaries.csv")

### 2. Exploration visuelle des données
#votre code 
st.title("📊 Visualisation des Salaires en Data Science")
st.markdown("Explorez les tendances des salaires à travers différentes visualisations interactives.")


if st.checkbox("Afficher un aperçu des données"):
    st.write(df.head())


#Statistique générales avec describe pandas 
#votre code 
st.subheader("📌 Statistiques générales")
st.write(df.describe())


### 3. Distribution des salaires en France par rôle et niveau d'expérience, uilisant px.box et st.plotly_chart
#votre code 
st.subheader("📈 Distribution des salaires en France")
fig = px.box(df, x="job_title", y="salary_in_usd", color="experience_level",title="Distribution des salaires en fonction du rôle et du niveau d'expérience")
st.plotly_chart(fig)

### 4. Analyse des tendances de salaires :
#### Salaire moyen par catégorie : en choisisant une des : ['experience_level', 'employment_type', 'job_title', 'company_location'], utilisant px.bar et st.selectbox 
category = st.selectbox(
    "Choisissez la catégorie pour analyser les salaires moyens :",
    ['experience_level', 'employment_type', 'job_title', 'company_location']
)

salary_by_category = df.groupby(category)['salary'].mean().reset_index()

fig = px.bar(salary_by_category, x=category, y="salary",title="Analyse des tendances de salaire",labels=category,color=category)

st.plotly_chart(fig)

### 5. Corrélation entre variables
# Sélectionner uniquement les colonnes numériques pour la corrélation
#votre code 

colonnes_numeriques = df[["salary", "salary_in_usd", "remote_ratio"]]

# Calcul de la matrice de corrélation
#votre code
corr_matrix = colonnes_numeriques.corr()

# Affichage du heatmap avec sns.heatmap 
#votre code 
st.subheader("🔗 Corrélations entre variables numériques")

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap="YlGnBu", fmt=".2f", cbar=True)

# Afficher le graphique dans Streamlit
st.pyplot(plt)


### 6. Analyse interactive des variations de salaire
# Une évolution des salaires pour les 10 postes les plus courants
job_counts = df["job_title"].value_counts().reset_index()

# count of job titles pour selectionner les postes
top_10_jobs = job_counts.head(10)
filtered_df = df[df["job_title"].isin(top_10_jobs["job_title"])]


# calcul du salaire moyen par an
salary_by_job = filtered_df.groupby(["job_title", "experience_level"])["salary_in_usd"].mean().reset_index()
experience_order = ["EN", "MI", "EX", "SE"]
salary_by_job["experience_level"] = pd.Categorical(salary_by_job["experience_level"], categories=experience_order, ordered=True)

salary_by_job = salary_by_job.sort_values(by="experience_level")
#utilisez px.line
fig = px.line(salary_by_job, 
              x="experience_level", 
              y="salary_in_usd", 
              color="job_title", 
              markers=True, 
              title="Évolution des salaires pour les 10 postes les plus courants",
              category_orders={"experience_level": experience_order})
#votre code 
st.subheader("📊 Évolution des salaires pour les 10 postes les plus courants")
st.plotly_chart(fig)




### 7. Salaire médian par expérience et taille d'entreprise
# utilisez median(), px.bar
#votre code 




### 8. Ajout de filtres dynamiques
#Filtrer les données par salaire utilisant st.slider pour selectionner les plages 
#votre code 




### 9.  Impact du télétravail sur le salaire selon le pays




### 10. Filtrage avancé des données avec deux st.multiselect, un qui indique "Sélectionnez le niveau d'expérience" et l'autre "Sélectionnez la taille d'entreprise"
#votre code 

