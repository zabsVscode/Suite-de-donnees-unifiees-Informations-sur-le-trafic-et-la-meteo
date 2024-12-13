# Projet de Prédiction de Trafic en Temps Réel

Ce projet utilise l'API de TomTom pour récupérer des données de trafic en temps réel sous forme de tuiles vectorielles. Les données récupérées peuvent être analysées pour identifier les incidents de trafic sur une carte.

## Structure du Projet

Le projet comprend les fichiers suivants :

- `config.json`: Fichier de configuration contenant l'URL de base de l'API, la clé API et le numéro de version.
- `vector_tiles.py`: Script principal pour interroger l'API et récupérer les tuiles vectorielles d'incidents de trafic.
- `analyze_tile.py`: Script pour analyser les tuiles récupérées et générer une carte.
- `tile_data.pbf`: Fichier contenant les données de la tuile récupérée.

## Description du Script `vector_tiles.py`

Ce script est responsable de l'interrogation de l'API pour récupérer les tuiles vectorielles. Voici les principales fonctionnalités :

- **Chargement de la configuration** : Le script charge les paramètres de configuration à partir d'un fichier JSON.
- **Requête API** : Il construit l'URL de la requête en fonction des paramètres de zoom, x, y, et des tags d'incidents (comme `delay` et `road_type`).
- **Gestion des erreurs** : Si une requête échoue, le script journalise l'erreur.

### Logique de la Requête

La requête est envoyée à l'API en utilisant la méthode GET, avec les paramètres suivants :

- `zoom`: Niveau de zoom de la tuile.
- `x`: Coordonnée X de la tuile.
- `y`: Coordonnée Y de la tuile.
- `key`: Clé API.
- `t`: Modèle de trafic (facultatif).

### Affichage des Logs

Le script utilise le module `logging` pour afficher les informations sur le processus, y compris :

- L'URL de la requête et les paramètres utilisés.
- L'état de la réponse (succès ou échec).
- Le contenu brut de la réponse pour aider au débogage.

## Analyse des Tuiles

Le script `analyze_tile.py` est conçu pour analyser les tuiles vectorielles récupérées et générer une carte. Actuellement, il affiche un message indiquant que la couche est vide lorsque les données ne sont pas présentes.

## Problèmes Rencontrés

### Erreurs de Requête

Lors des tests, nous avons rencontré des problèmes similaires avec deux API différentes. Les principaux symptômes observés incluent :

- Les tuiles récupérées contiennent des données vides.
- Les messages d'erreur indiquent que les paramètres de requête peuvent être incorrects.

### Solutions Potentielles

- **Vérification des Paramètres** : S'assurer que les paramètres envoyés dans la requête respectent la documentation de l'API.
- **Changement d'API** : Envisager de passer à une autre API pour récupérer les données de trafic.

## Conclusion

Ce projet vise à collecter et analyser des données de trafic en temps réel à l'aide de l'API de TomTom. Malgré les problèmes rencontrés avec les requêtes, les fonctionnalités de base sont en place. Nous continuerons à explorer d'autres API ou à attendre des corrections potentielles de celles-ci.