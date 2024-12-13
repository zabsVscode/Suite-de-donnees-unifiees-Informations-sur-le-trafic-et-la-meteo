import sys
import os

# Ajouter le dossier src au chemin d'accès des modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

try:
    from data.api import WeatherAPI
    print("Importation réussie de WeatherAPI")
except ImportError as e:
    print(f"Erreur d'importation : {e}")


def generate_alerts(weather_data):
    try:
        alerts = []

        # Affichage des données météo pour débogage
        print("Données météo reçues :")
        print(weather_data)  # Affiche tout le contenu des données météo

        # Vérification et alerte pour les vents forts
        wind_speed = weather_data.get("wind", {}).get("speed", 0)
        print(f"Vitesse du vent : {wind_speed} m/s")  # Affichage du vent pour débogage
        if wind_speed > 20:
            alerts.append(f"Alerte : Vents forts (Vitesse : {wind_speed} m/s)")

        # Vérification et alerte pour les fortes précipitations
        rain = weather_data.get("rain", {}).get("1h", 0)
        print(f"Précipitations sur 1 heure : {rain} mm")  # Affichage des précipitations pour débogage
        if rain > 10:
            alerts.append(f"Alerte : Fortes précipitations (Pluie : {rain} mm)")

        # Vérification et alerte pour les orages
        weather_main = weather_data.get("weather", [{}])[0].get("main")
        print(f"Condition météo principale : {weather_main}")  # Affichage de la condition météo pour débogage
        if weather_main == "Thunderstorm":
            alerts.append("Alerte : Orage")

        # Message de débogage des alertes générées
        if alerts:
            print(f"Alertes générées : {alerts}")
        else:
            print("Aucune alerte générée.")
        
        return alerts

    except Exception as e:
        print(f"Erreur lors de la génération des alertes : {e}")
        return []


if __name__ == "__main__":
    # Paramètres pour l'API
    username = "anthonyabs"  # Remplace par ton nom d'utilisateur GeoNames
    api_key = "OPENWEATHER_API_KEY"  # Remplace par ta clé API OpenWeather (n'oublie pas de la remplacer par ta vraie clé)
    city = "Paris"  # Ville pour récupérer les données météo

    # Créer une instance de l'API
    weather_api = WeatherAPI(username=username, api_key=api_key)
    
    # Récupérer les données météo pour la ville spécifiée
    weather_data = weather_api.fetch_weather_data(city)

    # Vérifier si les données ont été récupérées avec succès
    if weather_data:
        # Générer des alertes en fonction des données météo récupérées
        alerts = generate_alerts(weather_data)
    else:
        print("Impossible de récupérer les données météo.")
