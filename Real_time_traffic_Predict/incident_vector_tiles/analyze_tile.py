import mapbox_vector_tile
import folium

def load_tile_data(file_path):
    """Charge les données de la tuile à partir d'un fichier PBF."""
    with open(file_path, 'rb') as f:
        return f.read()

def decode_tile(tile_data):
    """Décode les données PBF en utilisant mapbox_vector_tile."""
    return mapbox_vector_tile.decode(tile_data)

def create_map(decoded_tile):
    """Crée une carte Folium et y ajoute des points d'incidents."""
    # Exemple de coordonnées de centre de la carte
    m = folium.Map(location=[45.0, -73.0], zoom_start=12)

    print(f"Nombre de couches décodées : {len(decoded_tile)}")
    for layer_name, layer in decoded_tile.items():
        print(f"Layer: {layer_name}, Nombre de fonctionnalités: {len(layer['features'])}")
        for feature in layer['features']:
            # Exemple d'extraction des coordonnées et d'ajout à la carte
            geometry = feature['geometry']
            if geometry['type'] == 'Point':
                coords = geometry['coordinates']
                folium.Marker(location=[coords[1], coords[0]], popup=str(feature)).add_to(m)

    return m


def main():
    # Chemin vers le fichier PBF
    file_path = 'tile_data.pbf'
    
    # Charger et décoder la tuile
    tile_data = load_tile_data(file_path)
    decoded_tile = decode_tile(tile_data)
    
    # Créer la carte et l'enregistrer
    traffic_map = create_map(decoded_tile)
    traffic_map.save('traffic_map.html')
    print("La carte a été enregistrée sous traffic_map.html.")

if __name__ == "__main__":
    main()
