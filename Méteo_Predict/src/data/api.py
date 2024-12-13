import os
import requests

class WeatherAPI:
    def __init__(self, username, api_key=None):
        self.username = username
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")  # Utilise la clé API si fournie, sinon récupère celle de l'environnement
        self.base_geonames_url = "http://api.geonames.org"
        self.base_openweather_url = "http://api.openweathermap.org/data/2.5/weather"

    def fetch_country_code(self, lat, lng):
        url = f"{self.base_geonames_url}/countryCode?lat={lat}&lng={lng}&username={self.username}&type=json"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Vérifie si la requête a échoué

            country_data = response.json()

            # Vérifier si les données sont valides avant d'extraire les informations
            if 'countryCode' in country_data and 'countryName' in country_data:
                return country_data['countryCode'], country_data['countryName']
            else:
                print(f"Données géonames invalides : {country_data}")
                return None, None
        except requests.exceptions.RequestException as e:
            print(f"Erreur de requête dans fetch_country_code pour {lat}, {lng}: {e}")
        return None, None

    def fetch_weather_data(self, city):
        url = f"{self.base_openweather_url}?q={city}&appid={self.api_key}&units=metric"  # Températures en Celsius
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Vérifie si la requête a échoué

            if response.ok:
                weather_data = response.json()
                # Vérifier si les données météo sont complètes
                if 'main' in weather_data and 'weather' in weather_data:
                    return weather_data
                else:
                    print(f"Données météo invalides pour la ville : {city}")
                    return None
            else:
                print(f"Erreur dans la récupération des données météo pour {city}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erreur de requête dans fetch_weather_data pour {city}: {e}")
        return None

    def fetch_zone_ids(self):
        url = "https://api.weather.gov/zones"
        headers = {
            'User-Agent': 'myweatherapp.com, contact@myweatherapp.com'
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Vérifie si la requête a échoué

            if response.ok:
                return response.json()
            else:
                print(f"Erreur dans la récupération des zones : {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erreur de requête dans fetch_zone_ids : {e}")
        return None
