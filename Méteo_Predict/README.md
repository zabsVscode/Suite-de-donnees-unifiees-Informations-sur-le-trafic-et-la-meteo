# Projet de Prédiction Météo

## Description
Ce projet utilise des API pour prédire la météo en Europe.

## Installation
1. Clone le repository.
2. Installe les dépendances avec `pip install -r requirements.txt`.

## Utilisation
1. Exécute `python src/main.py` pour commencer.

# Optimisation des Scripts pour Robots Autonomes

## 1. download.py
- Récupère les données météo d'une ville via l'API OpenWeather.
- Suggestions : Gestion des erreurs centralisée, unification des données dans une structure unique.

## 2. preprocess.py
- Interroge l'API NWS pour les prévisions météo.
- Suggestions : Centraliser la gestion des requêtes et extraire des données de manière uniforme.

## 3. city_data.py
- Récupère le code pays basé sur la latitude et la longitude.
- Suggestions : Valider les coordonnées avant appel API, utiliser une gestion d'erreurs centralisée.

## 4. zone_id.py
- Récupère les identifiants de zones météo.
- Suggestions : Centraliser les appels d'API, formater les réponses de manière uniforme.

## Optimisations Générales
- Créer un module API (`api_utils.py`) pour gérer les requêtes.
- Utiliser des structures de données unifiées pour les informations météorologiques.
- Documenter chaque fonction pour faciliter les modifications futures.

--------------------------------------------------------------------------------------------------------------------------------------------------------------

# Les fonctions des fichiers Python


## Fonctionnalitée possible de #geo_nav.py

1. Éviter des Obstacles
Définir des Zones d'Opération : La fonction is_in_france(lat, lon) vérifie si les coordonnées données sont dans une zone spécifiée (dans ce cas, la France). Si les coordonnées sont en dehors des limites, tu peux programmer le robot pour qu'il n'y accède pas. Cela permet de restreindre ses mouvements à un périmètre souhaité, évitant ainsi les obstacles en dehors de cette zone.
2. Système de Navigation
Navigation Basée sur les Coordonnées : En intégrant des coordonnées GPS, ton robot peut utiliser un système de navigation qui le guide d'un point à un autre à l'intérieur de la zone d'opération définie. Par exemple, s'il doit se déplacer d'un point A à un point B en France, il peut suivre les coordonnées jusqu'à sa destination.
3. Connaître sa Zone Géographique
Accès aux Données Pays : Le code utilise l'API GeoNames pour obtenir des informations sur le pays associé aux coordonnées. Cela pourrait être utile pour des décisions contextuelles, comme savoir quelles règles de fonctionnement s'appliquent, ou même quelles permissions sont nécessaires pour opérer dans certaines zones.
4. Accéder à des Données Météorologiques
Intégration avec OpenWeather : En ayant la latitude et la longitude, tu peux facilement faire des requêtes à une API météo comme OpenWeather pour obtenir des informations sur les conditions actuelles (température, précipitations, vitesse du vent, etc.). Cela te permettra d’ajuster le comportement du robot en fonction des conditions climatiques, par exemple en ralentissant ses mouvements en cas de pluie ou en évitant de sortir en cas de tempête.
5. Suivi en Temps Réel
Localisation et Suivi : En intégrant un module GPS à ton robot, il pourra transmettre sa position actuelle (latitude et longitude) en temps réel. Cela permettrait de suivre sa localisation à tout moment, ce qui est essentiel pour les interventions humaines ou les ajustements de mission. Tu pourrais également loguer ces données pour des analyses ultérieures sur son comportement dans différents environnements.
