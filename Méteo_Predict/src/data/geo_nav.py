import os
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

def fetch_country_code(username, lat, lng):
    """
    Récupère le code et le nom du pays à partir des coordonnées GPS.
    """
    url = f"http://api.geonames.org/countryCode?lat={lat}&lng={lng}&username={username}&type=json"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie si la requête a échoué
        country_data = response.json()

        # Vérification de la validité des données retournées
        country_code = country_data.get('countryCode')
        country_name = country_data.get('countryName')

        if not country_code or not country_name:
            print(f"Avertissement : Données incomplètes reçues pour la requête aux coordonnées ({lat}, {lng}).")
            return None, None
        
        return country_code, country_name

    except requests.exceptions.HTTPError as err:
        print(f"Erreur HTTP dans fetch_country_code : {err} - Code de statut : {err.response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur de requête dans fetch_country_code : {e}")
    except Exception as e:
        print(f"Erreur inattendue dans fetch_country_code : {e}")

    return None, None

def is_in_france(lat, lon):
    """
    Vérifie si les coordonnées sont dans les limites géographiques de la France métropolitaine.
    """
    try:
        if 41.303 <= lat <= 51.124 and -5.143 <= lon <= 9.600:
            return True
        else:
            return False
    except Exception as e:
        print(f"Erreur lors de la vérification des coordonnées dans is_in_france : {e}")
        return False

if __name__ == "__main__":
    try:
        geo_username = os.getenv("GEONAMES_USERNAME")
        api_key = os.getenv("OPENWEATHER_API_KEY")

        # Vérification de la présence des variables d'environnement
        if not geo_username:
            print("Erreur : le nom d'utilisateur GeoNames n'est pas défini dans les variables d'environnement.")
            exit(1)  # Quitte le script si la variable n'est pas définie
        
        if not api_key:
            print("Erreur : la clé API GeoNames n'est pas définie dans les variables d'environnement.")
            exit(1)  # Quitte le script si la variable n'est pas définie

        # Exemple de coordonnées de Paris
        latitude = 48.8566
        longitude = 2.3522

        if is_in_france(latitude, longitude):
            country_code, country_name = fetch_country_code(geo_username, latitude, longitude)
            
            if country_code:
                print(f"Code ISO du pays: {country_code}")
                print(f"Nom du pays: {country_name}")
            else:
                print("Aucune information de code pays trouvée.")
        else:
            print("Les coordonnées ne sont pas dans les limites de la France.")

    except Exception as e:
        print(f"Erreur générale dans le script : {e}")
        exit(1)
