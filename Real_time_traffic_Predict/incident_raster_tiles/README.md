# Projet Incident Raster Tiles

Ce projet utilise l'API TomTom pour générer des cartes de trafic en temps réel ou basées sur des données historiques, incluant des superpositions d'incidents de circulation sous forme de tuiles raster. Les cartes affichent des routes avec différentes couleurs pour indiquer les conditions de circulation.

## Légende des Couleurs sur la Carte

Cette carte utilise différentes couleurs pour indiquer les conditions de circulation. Voici la signification des couleurs utilisées :

- **Rouge** : Trafic très dense
- **Orange** : Trafic modéré
- **Vert** : Circulation fluide
- **Noir** : Route fermée

Ces couleurs sont générées en temps réel (ou à partir de données historiques) à partir de l'API TomTom.

## Installation

Pour utiliser ce projet, vous aurez besoin de Python 3.x et des bibliothèques suivantes :

- `requests`
- `Pillow`
- `numpy`

Vous pouvez installer les dépendances nécessaires en utilisant pip :

```bash
pip install requests Pillow numpy

## Configuration

Avant de lancer le script, assurez-vous de configurer votre fichier config.json avec votre clé API TomTom et les paramètres de votre carte.

{
    "baseURL": "https://api.tomtom.com",
    "versionNumber": "4",
    "style": "s0",
    "zoom": 13,
    "format": "png",
    "api_key": "brnxHJkxyCWHiIW0vIc4WflnG3RxGO0W",
    "latitude": 48.8566,
    "longitude": 2.3522
}

## Utilisation

Pour générer les tuiles raster et la carte HTML, exécutez le script Python :

" python raster_tiles.py "

# Après exécution, le script générera :

traffic_tile.png: La tuile de trafic.
traffic_map.html: La carte HTML avec la superposition de trafic.