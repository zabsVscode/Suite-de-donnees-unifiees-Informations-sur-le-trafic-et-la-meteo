import requests
import json
import sys

def load_config(file_path='config.json'):
    """Charge la configuration depuis le fichier JSON."""
    try:
        with open(file_path) as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Erreur : Le fichier de configuration '{file_path}' est introuvable.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Erreur : Le fichier de configuration n'est pas un JSON valide.")
        sys.exit(1)

def get_incident_viewport(api_key, base_url, version, bounding_box, bounding_zoom, overview_box, overview_zoom):
    """Effectue une requête pour obtenir les informations de la fenêtre d'affichage des incidents."""
    url = f"{base_url}/traffic/services/{version}/incidentViewport/{bounding_box}/{bounding_zoom}/{overview_box}/{overview_zoom}/true/json?key={api_key}"
    print(f"URL de la requête incidentViewport : {url}")  # Debug: afficher l'URL utilisée

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erreur lors de la requête : {e}")
        if e.response is not None:
            print(f"Contenu de la réponse : {e.response.text}")  # Afficher la réponse complète en cas d'erreur
        return None

def get_incidents(api_key, base_url, version, bounding_box, bounding_zoom, traffic_model_id):
    """Effectue une requête pour obtenir des informations sur les incidents."""
    url = f"{base_url}/traffic/services/{version}/incidents/{bounding_box}/{bounding_zoom}?key={api_key}&trafficModelId={traffic_model_id}"
    print(f"URL de la requête incidents : {url}")  # Debug: afficher l'URL utilisée

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erreur lors de la requête : {e}")
        if e.response is not None:
            print(f"Contenu de la réponse : {e.response.text}")  # Afficher la réponse complète
        return None

def generate_map(incident_data):
    """Génère un fichier HTML pour afficher les incidents sur une carte."""
    with open("incident_map.html", "w") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Carte de Trafic</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <style>
        html, body {
            height: 100%;
            margin: 0;
        }
        #map {
            height: 100%;
            width: 100%;
        }
    </style>
</head>
<body>
    <div id="map"></div>
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <script>
        var map = L.map('map').setView([46.6034, 1.8883], 5); // Coordonnées centrées sur la France

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap'
        }).addTo(map);
""")

        if 'incidents' in incident_data:
            incidents = incident_data['incidents']
            for incident in incidents:
                # Vérifiez si latitude et longitude sont présents
                if 'latitude' in incident and 'longitude' in incident:
                    lat = incident['latitude']
                    lon = incident['longitude']
                    severity = incident.get('severity', 'medium')
                    color = 'red' if severity == 'high' else 'orange' if severity == 'medium' else 'green'

                    f.write(f"""
        L.circleMarker([{lat}, {lon}], {{
            radius: 8,
            color: '{color}',
            fillOpacity: 0.5
        }}).addTo(map).bindPopup("Incident: {severity}");
""")

        f.write("""        
    </script>
</body>
</html>
""")

if __name__ == "__main__":
    config = load_config()

    # Définir une bounding box qui couvre toute la France
    bounding_box = "-5.1425,41.3035,9.5632,51.1247"
    bounding_zoom = 10  # Zoom pour voir plus d'incidents
    overview_box = bounding_box
    overview_zoom = bounding_zoom

    # Récupérer les informations de la fenêtre d'affichage des incidents
    incident_viewport_data = get_incident_viewport(config['api_key'], config['base_url'], config['version'], bounding_box, bounding_zoom, overview_box, overview_zoom)

    if incident_viewport_data:
        print(json.dumps(incident_viewport_data, indent=4))  # Afficher les données de la fenêtre d'affichage

        # Extraire l'ID du modèle de trafic
        traffic_model_id = incident_viewport_data['viewpResp']['trafficState']['@trafficModelId']

        # Récupérer les incidents réels en utilisant l'ID du modèle de trafic
        incident_data = get_incidents(config['api_key'], config['base_url'], config['version'], bounding_box, bounding_zoom, traffic_model_id)

        if incident_data:
            print(json.dumps(incident_data, indent=4))  # Afficher les données des incidents
            if 'incidents' in incident_data and incident_data['incidents']:
                generate_map(incident_data)  # Générer la carte HTML
            else:
                print("Aucun incident trouvé.")
        else:
            print("Erreur lors de la récupération des incidents.")
    else:
        print("Erreur lors de la récupération des informations de la fenêtre d'affichage.")
