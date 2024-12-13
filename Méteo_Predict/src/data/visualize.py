import folium
import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Coordonnées fixes de Paris (en cas d'échec de l'API)
fixed_city_data = {
    "Paris": {"lat": 48.8566, "lon": 2.3522},
    "Marseille": {"lat": 43.2965, "lon": 5.3698},
    "Lyon": {"lat": 45.7640, "lon": 4.8357}
}

# Fonction pour récupérer les alertes météo via OpenWeather (prépare pour l'abonnement payant)
def fetch_weather_alerts(lat, lon, api_key):
    url = f"http://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=hourly,daily&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()

        # Vérification de la présence d'alertes
        if 'alerts' in weather_data:
            return weather_data['alerts']
        else:
            print(f"Aucune alerte pour les coordonnées {lat}, {lon}.")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des alertes pour {lat}, {lon} : {e}")
        return []


# Fonction pour récupérer les données de la ville via GeoNames
def fetch_city_data(city_name, country_code, geo_username):
    url = f"http://api.geonames.org/searchJSON?placename={city_name}&country={country_code}&username={geo_username}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Vérification de la validité des données retournées
        if 'geonames' in data and data['geonames']:
            return data['geonames'][0]  # Retourne la première ville trouvée
        else:
            print(f"Aucune donnée géographique trouvée pour la ville {city_name}.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des données pour la ville {city_name} : {e}")
        return None

# Fonction pour créer la carte météo
def create_weather_map(city_data, api_key, geo_username):
    try:
        if not city_data or not isinstance(city_data, list):
            raise ValueError("city_data est vide ou non valide.")
        
        print("Création de la carte météo...")  # Message de confirmation

        # Centrer la carte sur la France par défaut
        map_obj = folium.Map(location=[46.603354, 1.888334], zoom_start=5)

        # Ajouter un marqueur pour chaque ville
        for city in city_data:
            city_name = city.get("name")
            lat = city.get("lat")
            lon = city.get("lon")

            # Vérification et conversion des coordonnées
            try:
                lat = float(lat)
                lon = float(lon)
            except ValueError:
                print(f"Erreur : Coordonnées non valides pour la ville {city_name}.")
                continue

            if lat is None or lon is None:
                print(f"Erreur : Coordonnées manquantes pour la ville {city_name}.")
                continue

            # Vérification des coordonnées valides
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                print(f"Erreur : Coordonnées invalides pour {city_name} ({lat}, {lon}).")
                continue

            # Récupérer les alertes météo (en prévision de l'abonnement payant)
            alerts = fetch_weather_alerts(lat, lon, api_key)
            alert_message = "\n".join([alert['description'] for alert in alerts]) if alerts else "Pas d'alerte"

            # Ajouter un marqueur sur la carte
            folium.Marker(
                location=[lat, lon],
                popup=f"{city_name}\n{alert_message}",
                icon=folium.Icon(color="red" if alerts else "blue")
            ).add_to(map_obj)

        # Sauvegarder la carte en HTML
        try:
            map_obj.save("carte_meteo_alertes.html")
            print("Carte HTML créée : 'carte_meteo_alertes.html'")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la carte HTML : {e}")

    except Exception as e:
        print(f"Erreur lors de la génération de la carte : {e}")

# Code principal pour exécuter la création de la carte
if __name__ == "__main__":
    geo_username = os.getenv("GEONAMES_USERNAME")  # Utilise ton nom d'utilisateur GeoNames
    api_key = os.getenv("OPENWEATHER_API_KEY")  # Clé API OpenWeatherMap

    if not geo_username:
        print("Erreur : Le nom d'utilisateur GeoNames n'est pas défini.")
        exit(1)
    
    if not api_key:
        print("Erreur : La clé API OpenWeatherMap n'est pas définie.")
        exit(1)

    # Liste des villes pour lesquelles tu veux afficher les alertes
    city_names = ["Paris", "Marseille", "Lyon"]
    country_code = "FR"  # Code pays pour la France

    # Récupérer les données des villes via GeoNames
    city_data = []
    for city_name in city_names:
        city = fetch_city_data(city_name, country_code, geo_username)
        if city:
            city_data.append({
                "name": city_name,
                "lat": city.get("lat"),
                "lon": city.get("lng")
            })
        else:
            # Utiliser les coordonnées fixes en cas d'échec
            if city_name in fixed_city_data:
                city_data.append({
                    "name": city_name,
                    "lat": fixed_city_data[city_name]["lat"],
                    "lon": fixed_city_data[city_name]["lon"]
                })

    # Créer la carte avec les données récupérées
    create_weather_map(city_data, api_key, geo_username)
