import requests 
import json
import logging

# Configuration de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VectorTilesAPI:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.base_url = self.config['baseURL']
        self.api_key = self.config['apiKey']
        self.version = self.config['versionNumber']
    
    def load_config(self, config_path):
        """Charge la configuration à partir d'un fichier JSON."""
        try:
            with open(config_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logging.error("Le fichier de configuration n'a pas été trouvé.")
            raise
        except json.JSONDecodeError:
            logging.error("Erreur lors du décodage du fichier JSON.")
            raise
    
    def get_vector_tile(self, zoom, x, y, tags=None, traffic_model_id=-1):
        """Récupère une tuile vectorielle d'incidents de trafic."""
        
        # Vérification des valeurs de zoom, x et y
        if not (0 <= zoom <= 22):
            raise ValueError(f"Zoom doit être entre 0 et 22, mais reçu {zoom}.")
        
        max_coordinate = 2 ** zoom - 1
        
        if not (0 <= x <= max_coordinate):
            raise ValueError(f"x doit être entre 0 et {max_coordinate}, mais reçu {x}.")
        
        if not (0 <= y <= max_coordinate):
            raise ValueError(f"y doit être entre 0 et {max_coordinate}, mais reçu {y}.")

        url = f"https://{self.base_url}/traffic/map/{self.version}/tile/incidents/{zoom}/{x}/{y}.pbf"
        params = {
            'key': self.api_key,
            't': traffic_model_id
        }

        if tags:
            # Formattage des tags pour l'API
            unique_tags = list(set(tags))  # Assurer que les tags sont uniques
            params['tags'] = f"[{','.join(unique_tags)}]"
        
        logging.info(f"Requête vers l'URL: {url} avec les paramètres: {params}")

        response = requests.get(url, params=params)

        if response.status_code == 200:
            logging.info("Requête réussie.")
            return response.content  # Renvoie le contenu binaire de la réponse
        else:
            logging.error(f"Erreur lors de la requête: {response.status_code} - {response.text}")
            raise Exception(f"Erreur lors de la récupération de la tuile : {response.text}")

if __name__ == "__main__":
    api = VectorTilesAPI('config.json')
    # Exemple de requête pour la tuile (zoom, x, y)
    try:
        tile_data = api.get_vector_tile(zoom=5, x=4, y=8, tags=["delay", "road_type"])
        # Traitement de tile_data (par exemple, stockage ou analyse)
        with open('tile_data.pbf', 'wb') as f:
            f.write(tile_data)
        logging.info("Les données de la tuile ont été enregistrées avec succès.")
    except Exception as e:
        logging.error(f"Une erreur s'est produite: {str(e)}")
