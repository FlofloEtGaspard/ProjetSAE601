"""
Lien vers notre Github : https://github.com/FlofloEtGaspard/ProjetSAE601/tree/main
Florian Bougon et Gaspard Louvel
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
df = pd.read_csv("C:\\Users\\bougo\\Documents\\Eudes\\data\\ds_salaries.csv")

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

# Affichage du graphique
fig = px.bar(salary_by_category, x=category, y="salary",title="Analyse des tendances de salaire",labels=category,color=category)

st.plotly_chart(fig)

st.markdown("Nous pouvons voir ici les salaires moyens par rapport à différentes catégories: l'expérience, le type de job, le type de contrat et le pays. Nous remarquons de grandes différences entre certaines alors que d'autres sont assez similaires.") 

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

# Affichage du graphique
st.pyplot(plt)

st.markdown("Nous voyons qu'il n'y a aucune corrélation entre les variables numériques.")

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

st.markdown("Nous remarquons que le salaire moyen augmente tout au long de la carrière hormis pour certains jobs ou il baisse puis remonte ensuite. Cela peut etre du à un biais venant des autres variables comme par exemple le pays ou encore le ratio de télétravail.")


### 7. Salaire médian par expérience et taille d'entreprise
# utilisez median(), px.bar
#votre code 
salaire_median = df.groupby(["experience_level", "company_size"])["salary_in_usd"].median().reset_index()

fig = px.bar(salaire_median, 
             x="experience_level", 
             y="salary_in_usd", 
             color="company_size", 
             barmode="group", 
             title="Salaire médian par niveau d'expérience et taille d'entreprise",
             labels={"salary_in_usd": "Salaire médian (USD)", "experience_level": "Niveau d'expérience"},
             category_orders={"experience_level": ["EN", "MI", "EX", "SE"]})

st.subheader("📊 Salaire médian par niveau d'expérience et taille d'entreprise")
st.plotly_chart(fig)

st.markdown("Nous voyons que le salaire médian a tendance à être plus élevé dans les entreprises de moyenne taille excepté pour les séniors ou les grandes compagnies payent mieux.")

### 8. Ajout de filtres dynamiques
#Filtrer les données par salaire utilisant st.slider pour selectionner les plages 
#votre code 

# Définition des sliders
min_salaire, max_salaire = st.slider(
    "Filtrer les données par salaire", 
    min_value=int(df["salary_in_usd"].min()), 
    max_value=int(df["salary_in_usd"].max()), 
    value=(int(df["salary_in_usd"].min()), int(df["salary_in_usd"].max())),
    step=1000
)

# Filtrage du dataset en fonction des sliders
filtered_df = df[(df["salary_in_usd"] >= min_salaire) & (df["salary_in_usd"] <= max_salaire)]

st.dataframe(filtered_df)

### 9.  Impact du télétravail sur le salaire selon le pays

df_teletravail = df[df["remote_ratio"].notna()]
df_teletravail["remote_work"] = df_teletravail["remote_ratio"].map({0: "Présentiel", 50: "Hybride", 100: "Télétravail"})

# Regrouper les salaires moyens par pays et mode de travail
salaire_tele_par_pays = df_teletravail.groupby(["employee_residence", "remote_work"])["salary_in_usd"].mean().reset_index()

# Affichage du graphique
fig = px.bar(salaire_tele_par_pays, 
             x="employee_residence", 
             y="salary_in_usd", 
             color="remote_work", 
             title="Impact du télétravail sur le salaire selon le pays",
             labels={"employee_residence": "Pays", "salary_in_usd": "Salaire moyen (USD)", "remote_work": "Type de travail"},
             barmode="group")

# Afficher le graphique avec Streamlit
st.plotly_chart(fig)

### 10. Filtrage avancé des données avec deux st.multiselect, un qui indique "Sélectionnez le niveau d'expérience" et l'autre "Sélectionnez la taille d'entreprise"
#votre code 
st.subheader("📊 Filtrage avancé des donnée")

experience_options = df["experience_level"].unique().tolist()
company_size_options = df["company_size"].unique().tolist()

# Création des widgets pour filtrer
selected_experience = st.multiselect("Sélectionnez le niveau d'expérience", experience_options, default=experience_options)
selected_company_size = st.multiselect("Sélectionnez la taille d'entreprise", company_size_options, default=company_size_options)

# Filtrage des données puis affichage
filtered_df = df[(df["experience_level"].isin(selected_experience)) & 
                 (df["company_size"].isin(selected_company_size))]

st.dataframe(filtered_df)
