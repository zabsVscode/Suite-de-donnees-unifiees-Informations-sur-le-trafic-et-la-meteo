# Constantes pour les limites géographiques de la France
LAT_MIN, LAT_MAX = 41.303, 51.124
LON_MIN, LON_MAX = -5.143, 9.600

# Fonction pour vérifier si les coordonnées sont dans les limites de la France
def is_in_france(lat, lon):
    return LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX

def main():
    latitude = 48.8566  # Exemple de latitude pour Paris
    longitude = 2.3522  # Exemple de longitude pour Paris

    # Vérification si les coordonnées sont dans les limites de la France
    message = "Les coordonnées sont dans les limites de la France." if is_in_france(latitude, longitude) else "Les coordonnées ne sont pas dans les limites de la France."
    print(message)

if __name__ == "__main__":
    main()
