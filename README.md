# s c r a p _ e t l 
 # Projet ETL de Scraping pour Fromages

## Introduction

Le projet vise à créer un système ETL (Extraction, Transformation, et Chargement) spécialisé dans le scraping de données relatives aux fromages à partir d'un site web https://www.laboitedufromager.com/categorie-fromage/fromage/ . L'objectif est d'automatiser le processus d'extraction des informations telles que les prix, les noms et les photos des fromages, puis de les transformer et les charger dans une base de données.

## Fonctionnalités clés

1. **Extraction de Données :**
   - Le système sera capable de naviguer sur le site web cible et extraire de manière automatisée les informations pertinentes sur les fromages.
   - Les données extraites incluront les prix, les noms et les images des fromages.

2. **Transformation des Données :**
   - Les données extraites subiront des transformations pour assurer la cohérence et la qualité des informations.
   - La normalisation des noms de fromages, la conversion des prix dans une unité uniforme et la compression des images pour optimiser l'espace seront effectuées.

3. **Chargement dans la Base de Données :**
   - Une base de données sera créée pour stocker les données de manière organisée.
   - Le système ETL chargera les données transformées dans la base de données, en veillant à la cohérence et à l'intégrité des informations.

## Technologies Utilisées

1. **Scraping :**
   - Utilisation de bibliothèques telles que BeautifulSoup ou Scrapy pour extraire les données du site web.

2. **Transformation :**
   - Python sera utilisé pour la manipulation et la transformation des données. Pandas peut être utilisé pour cette tâche.

3. **Base de Données :**
   - sqlite3 peuvent être envisagés en fonction des besoins spécifiques du projet.

4. **Automatisation :**
   - L'utilisation de scripts et de planifications de tâches (cron jobs) assurera l'automatisation régulière du processus.

## Diagramme de Flux

1. **Extraction :**
   - Scraping des données à partir du site web.

2. **Transformation :**
   - Nettoyage, normalisation et conversion des données extraites.

3. **Chargement :**
   - Stockage des données transformées dans la base de données.

## Livraables

1. **Code Source :**
   - Fourniture du code source du système ETL.

2. **Documentation :**
   - Documentation détaillée du processus d'installation, de configuration et d'utilisation.

3. **Base de Données :**
   - Mise en place de la base de données avec un schéma bien défini.

## Conclusion

Le système ETL de scraping proposé automatisera efficacement la collecte, la transformation et le stockage des données sur les fromages à partir d'un site web, offrant ainsi une solution robuste pour la gestion de ces informations.

 
