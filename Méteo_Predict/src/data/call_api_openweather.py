import sys
import os
from dotenv import load_dotenv  # Importer la fonction pour charger le .env
import requests

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Ajoute le chemin parent au système de chemin
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.api import WeatherAPI  # Utilise un import absolu

if __name__ == "__main__":
    try:
        # Récupérer le nom d'utilisateur et la clé API à partir des variables d'environnement
        username = os.getenv("GEONAMES_USERNAME")
        api_key = os.getenv("OPENWEATHER_API_KEY")

        # Vérification des variables d'environnement
        if not username:
            print("Erreur : le nom d'utilisateur GeoNames n'est pas défini dans les variables d'environnement.")
            exit(1)  # Quitte le script si la variable n'est pas définie
        
        if not api_key:
            print("Erreur : la clé API GeoNames n'est pas définie dans les variables d'environnement.")
            exit(1)  # Quitte le script si la variable n'est pas définie

        # Créer une instance de l'API avec les paramètres
        weather_api = WeatherAPI(username=username, api_key=api_key)

        city = "Paris"  # Remplace par la ville que tu souhaites
        weather_data = weather_api.fetch_weather_data(city)

        # Vérifier si les données météo ont été récupérées avec succès
        if weather_data:
            print("Données Météorologiques :")
            print(f"Ville : {weather_data['name']}")
            print(f"Température : {weather_data['main']['temp']} °C")
            print(f"Conditions : {weather_data['weather'][0]['description']}")
            print(f"Humidité : {weather_data['main']['humidity']}%")
            print(f"Pression atmosphérique : {weather_data['main']['pressure']} hPa")

            # Gestion du vent - conversion m/s en km/h
            if 'wind' in weather_data:
                wind_speed_mps = weather_data['wind'].get('speed', 'Données indisponibles')
                wind_deg = weather_data['wind'].get('deg', 'Données indisponibles')
                
                # Convertir la vitesse du vent de m/s à km/h
                if isinstance(wind_speed_mps, (int, float)):  # Vérifie si la valeur est numérique
                    wind_speed_kmh = wind_speed_mps * 3.6  # Conversion de m/s à km/h
                    print(f"Vitesse du vent : {wind_speed_kmh:.2f} km/h")
                else:
                    print(f"Vitesse du vent : {wind_speed_mps}")
                
                print(f"Direction du vent : {wind_deg}°")
            else:
                print("Données sur le vent : Non disponibles")

            print(f"Visibilité : {weather_data.get('visibility', 'Non disponible')} mètres")

            # Vérifier les précipitations (pluie/neige)
            if 'rain' in weather_data:
                print(f"Pluie (dernière heure) : {weather_data['rain'].get('1h', 'Données indisponibles')} mm")
            else:
                print("Pluie : Pas de précipitations")

            if 'snow' in weather_data:
                print(f"Neige (dernière heure) : {weather_data['snow'].get('1h', 'Données indisponibles')} mm")
            else:
                print("Neige : Pas de précipitations")

            print(f"Couverture nuageuse : {weather_data['clouds']['all']}%")
        else:
            print("Aucune donnée disponible.")

    except requests.exceptions.RequestException as e:
        print(f"Erreur de requête dans la récupération des données météo : {e}")
    except KeyError as e:
        print(f"Erreur de traitement des données météo, clé manquante : {e}")
    except Exception as e:
        print(f"Une erreur imprévue s'est produite : {e}")
