import requests

def get_distance_matrix(origins, destinations):
    API_KEY = 'TON_API_KEY_GOOGLE'
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origins}&destinations={destinations}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        return data['rows'][0]['elements']
    return {"error": "Impossible de calculer les distances"}
