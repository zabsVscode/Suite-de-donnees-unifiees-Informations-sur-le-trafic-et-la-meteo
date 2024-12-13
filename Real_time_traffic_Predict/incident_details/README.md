markdown
Copier le code
# Incident Details API

## Description
Cette API fournit des informations sur les incidents de circulation dans une zone de délimitation donnée ou sur ceux qui l'intersectent. Elle utilise l'API TomTom pour obtenir des données sur différents types d'incidents, tels que des accidents, des congestions, et d'autres conditions routières.

## Utilisation

### Installation des Dépendances
Assurez-vous d'avoir installé les dépendances requises. Vous pouvez utiliser `pip` :

```bash
pip install requests folium

Configuration

Obtenez une clé API : Pour utiliser l'API TomTom, vous devez vous inscrire et obtenir une clé API.

Créez un fichier config.json : Ce fichier doit contenir votre clé API au format suivant :
json

{
    "api_key": "VOTRE_CLE_API"
}

Exécution du Script

Pour exécuter le script incident_details.py, assurez-vous d'être dans un environnement virtuel et que le fichier config.json est correctement configuré.

bash

python incident_details.py

Résultat

Le script génère une carte HTML (map.html) qui visualise les incidents de circulation dans la zone délimitée par les coordonnées fournies. Les incidents sont représentés par des lignes colorées, où chaque couleur correspond à un type d'incident :

1: Accident (Rouge)
2: Congestion (Orange)
3: Route fermée (Bleu)
4: Travaux (Vert)
5: Autre (Violet)
6: Catégorie 6 (Jaune)
7: Catégorie 7 (Marron)
8: Catégorie 8 (Rose)

Les types d'incidents sont également affichés sur la carte avec des marqueurs indiquant le type d'incident en fonction de sa catégorie.

Exemples de Résultats

Lorsque vous exécutez le script, vous devriez voir un fichier map.html contenant des informations sur les incidents dans la région spécifiée, avec des marqueurs et des lignes représentant les différents types d'incidents.

