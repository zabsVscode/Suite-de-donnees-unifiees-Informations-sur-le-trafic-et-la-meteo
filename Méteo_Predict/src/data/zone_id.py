######zone_id recupère les zones d'incendie en Amérique (utile?)

print("Début de zone_id.py")

from api import WeatherAPI  # Utilisation d'import absolu
import os  # Importer le module os pour accéder aux variables d'environnement

# Vérification de la présence de la clé API avant de procéder
api_key = os.getenv("OPENWEATHER_API_KEY")

# Vérification si la clé API est définie
if not api_key:
    print("Erreur : La clé API GeoNames n'est pas définie.")
    exit(1)

print("WeatherAPI importé avec succès.")

if __name__ == "__main__":
    username = "anthonyabs"  # Remplacer par ton nom d'utilisateur GeoNames
    weather_api = WeatherAPI(username=username, api_key=api_key)

    try:
        # Récupérer les données des zones
        zone_data = weather_api.fetch_zone_ids()
        
        # Afficher la réponse complète de l'API pour déboguer
        print("Données récupérées de l'API :", zone_data)

        # Vérification si des zones ont été trouvées
        if zone_data:
            zones = zone_data.get('zones', [])
            if zones:
                # Filtrer les zones pour n'inclure que celles qui sont en France
                france_zones = [zone for zone in zones if zone.get('countryCode') == 'FR']
                
                if france_zones:
                    for zone in france_zones:
                        print(f"Zone ID: {zone['id']}, Nom: {zone['name']}")
                else:
                    print("Aucune zone trouvée en France.")
            else:
                print("Aucune zone trouvée.")
        else:
            print("Erreur : Aucune donnée de zone disponible.")

    except Exception as e:
        # Gestion d'erreur si l'appel à l'API échoue
        print(f"Erreur lors de la récupération des zones : {e}")
