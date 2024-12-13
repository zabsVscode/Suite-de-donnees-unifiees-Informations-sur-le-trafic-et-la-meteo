import requests
import json
import folium

class IncidentDetailsAPI:
    def __init__(self, api_key, base_url="https://api.tomtom.com/traffic/services/5"):
        self.api_key = api_key
        self.base_url = base_url

    def get_incident_details_by_bbox(self, bbox, language='fr-FR', time_validity_filter='present', category_filter=None):
        params = {
            'key': self.api_key,
            'bbox': bbox,
            'language': language,
            'timeValidityFilter': time_validity_filter,
        }
        if category_filter:
            params['categoryFilter'] = category_filter
        
        response = requests.get(f"{self.base_url}/incidentDetails", params=params)
        return self.handle_response(response)

    def handle_response(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erreur lors de la requête : {response.status_code} - {response.text}")

# Dictionnaire des catégories d'incidents (en français)
incident_types = {
    0: "Inconnu",                      # Unknown
    1: "Accident",                     # Accident
    2: "Brouillard",                   # Fog
    3: "Conditions dangereuses",       # Dangerous Conditions
    4: "Pluie",                        # Rain
    5: "Glace",                        # Ice
    6: "Bouchon",                      # Jam (Congestion)
    7: "Voie fermée",                 # Lane Closed
    8: "Route fermée",                 # Road Closed
    9: "Travaux",                      # Road Works
    10: "Vent",                        # Wind
    11: "Inondation",                  # Flooding
    14: "Véhicule en panne"            # Broken Down Vehicle
}

# Exemple d'utilisation
if __name__ == "__main__":
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    
    api = IncidentDetailsAPI(api_key=config['api_key'])
    
    # Coordonnées de Paris, France
    bbox = "2.2241,48.8155,2.4699,48.9022"  # Coordonnées délimitant la zone de Paris
    
    try:
        incident_data = api.get_incident_details_by_bbox(bbox)
        print(json.dumps(incident_data, indent=4, ensure_ascii=False))  # Affichage des résultats
        
        # Créer la carte centrée sur Paris
        m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)  # Coordonnées de Paris

        # Définir les couleurs en fonction du type d'incident
        incident_colors = {
            0: 'gray',     # Inconnu
            1: 'red',      # Accident
            2: 'blue',     # Brouillard
            3: 'orange',   # Conditions dangereuses
            4: 'green',    # Pluie
            5: 'purple',   # Glace
            6: 'yellow',   # Bouchon (Congestion)
            7: 'brown',    # Voie fermée
            8: 'pink',     # Route fermée
            9: 'lightblue',# Travaux
            10: 'darkgreen', # Vent
            11: 'cyan',    # Inondation
            14: 'lightgray' # Véhicule en panne
        }

        # Vérifier si des incidents sont présents dans les données
        if 'incidents' in incident_data:
            for incident in incident_data['incidents']:
                # Vérifiez si les coordonnées sont disponibles
                if 'geometry' in incident and 'coordinates' in incident['geometry']:
                    coords = incident['geometry']['coordinates']
                    icon_category = incident['properties'].get('iconCategory', 0)
                    color = incident_colors.get(icon_category, 'gray')  # Couleur par défaut si non spécifiée
                    
                    # Ajout d'une ligne représentant l'incident
                    folium.PolyLine(locations=[(lat, lon) for lon, lat in coords], color=color).add_to(m)

                    # Ajout d'un marqueur au début de la ligne
                    start_point = coords[0]
                    folium.Marker(
                        location=(start_point[1], start_point[0]),  # Notez que latitude est en deuxième position
                        popup=f"Type d'incident: {incident_types.get(icon_category, 'Type inconnu')}",  # Afficher en français
                        icon=folium.Icon(color=color)
                    ).add_to(m)

        # Sauvegarder la carte en fichier HTML
        m.save('map.html')
        print("La carte a été sauvegardée sous le nom 'map.html'.")

    except Exception as e:
        print(e)
