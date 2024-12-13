import sys
import os
import time  # Importer le module time pour éviter l'erreur "time is not defined"

# Ajouter src au chemin de recherche des modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data.preprocess import fetch_forecast
from data.visualize import create_weather_map
from data.alerts import generate_alerts

def run_weather_monitor(city_name, api_key, geo_username, interval=900):  # Ajout du paramètre geo_username
    while True:
        print("Récupération des données météorologiques pour la ville:", city_name)
        forecast_data = fetch_forecast(city_name, api_key)
        alerts = generate_alerts(forecast_data)
        
        # Affichage détaillé des données récupérées
        print("\nDonnées météo récupérées :")
        print(f"Ville: {city_name}")
        print(f"Prévisions pour les 5 prochaines heures:")
        for hour_data in forecast_data['list']:
            time_of_data = hour_data['dt_txt']
            temperature = hour_data['main']['temp']
            description = hour_data['weather'][0]['description']
            wind_speed_mps = hour_data['wind']['speed']  # en m/s
            wind_speed_kmh = wind_speed_mps * 3.6  # Conversion en km/h
            wind_deg = hour_data['wind']['deg']
            humidity = hour_data['main']['humidity']
            pressure = hour_data['main']['pressure']
            
            print(f"\nHeure: {time_of_data}")
            print(f"Température: {temperature}°C")
            print(f"Description: {description}")
            print(f"Vitesse du vent: {wind_speed_kmh:.2f} km/h ({wind_speed_mps} m/s)")
            print(f"Direction du vent: {wind_deg}°")
            print(f"Humidité: {humidity}%")
            print(f"Pression: {pressure} hPa")

        # Affichage des alertes de type orage, pluie, etc.
        print("\nAlertes météo générées :")
        for alert in alerts:
            print(f"Type d'alerte: {alert['event']}")
            print(f"Description: {alert['description']}")
            print(f"Start: {alert['start']} / End: {alert['end']}")
        
        # Mise à jour de la carte avec l'ajout du paramètre geo_username
        create_weather_map([{"name": city_name, "lat": 48.8566, "lon": 2.3522}], alerts, geo_username=geo_username)
        
        print(f"\nCarte mise à jour avec les alertes. Nouvelle mise à jour dans {interval // 60} minutes.")
        time.sleep(interval)  # Attente avant la prochaine mise à jour

if __name__ == "__main__":
    api_key = os.getenv("OPENWEATHER_API_KEY")
    geo_username = os.getenv("GEO_USERNAME")  # Récupérez le geo_username depuis une variable d'environnement
    run_weather_monitor("Paris", api_key, geo_username)
