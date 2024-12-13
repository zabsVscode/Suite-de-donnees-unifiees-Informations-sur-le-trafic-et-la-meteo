import requests
import urllib.parse
import sys
import os

# Ajoute le chemin parent au système de chemin
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.api import WeatherAPI  # Utilisation d'import absolu

def fetch_forecast(city_name, api_key):
    """Récupère les prévisions météorologiques pour une ville donnée."""
    if not city_name or not api_key:
        print("Erreur : Le nom de la ville ou la clé API sont manquants.")
        return None

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={urllib.parse.quote(city_name)}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lève une exception pour les erreurs HTTP
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erreur {response.status_code} lors de la récupération des prévisions pour {city_name}.")
    except requests.exceptions.HTTPError as errh:
        print(f"Erreur HTTP: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Erreur de connexion: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Erreur inconnue: {err}")
    return None

def fetch_city_data(city_name, country_code, username):
    """Récupère les données de la ville avec le nom et le code pays via l'API GeoNames."""
    if not city_name or not country_code or not username:
        print("Erreur : Le nom de la ville, le code pays ou le nom d'utilisateur GeoNames sont manquants.")
        return None

    url = f"http://api.geonames.org/searchJSON?placename={urllib.parse.quote(city_name)}&country={country_code}&username={username}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erreur {response.status_code} lors de la récupération des données de la ville.")
    except requests.exceptions.RequestException as e:
        print(f"Erreur dans la récupération des villes : {e}")
    return None

def print_forecast_data(data):
    """Affiche les données des prévisions météorologiques si elles existent."""
    if data and 'list' in data:
        print("Prévisions Météorologiques (OpenWeatherMap) :")
        for period in data['list']:
            dt_txt = period['dt_txt']
            temp = period['main']['temp']
            weather_description = period['weather'][0]['description']
            print(f"{dt_txt}: Température: {temp}°C, Conditions: {weather_description}")
            print("-------------------------------------------------")
    else:
        print("Aucune donnée disponible ou format incorrect.")

if __name__ == "__main__":
    username = os.getenv("GEONAMES_USERNAME")  # Récupère le nom d'utilisateur GeoNames
    api_key = os.getenv("OPENWEATHER_API_KEY")  # Récupérer la clé API OpenWeatherMap depuis la variable d'environnement
    
    # Vérification de l'API key
    if not api_key:
        print("Erreur : La clé API OpenWeatherMap n'a pas été trouvée.")
        exit(1)  # Quitte le script si la clé API est manquante
    else:
        print(f"Clé API OpenWeatherMap détectée : {api_key}")  # Affichage pour la vérification

    # Remplace ici par le nom de la ville pour les prévisions
    city_name = "Paris"
    forecast_data = fetch_forecast(city_name, api_key)
    if forecast_data:
        print_forecast_data(forecast_data)
    else:
        print("Impossible de récupérer les prévisions pour la ville.")

    country_code = "FR"  # Code pays pour la France
    if username:
        city_data = fetch_city_data(city_name, country_code, username)
        if city_data:
            print(f"City data: {city_data}")
        else:
            print("Impossible de récupérer les données de la ville.")
    else:
        print("Erreur : Le nom d'utilisateur GeoNames est manquant.")
