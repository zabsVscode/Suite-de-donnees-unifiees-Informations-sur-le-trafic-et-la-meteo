import requests

def get_directions(origin, destination):
    API_KEY = 'API_KEY_GOOGLE'
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'OK':
        steps = data['routes'][0]['legs'][0]['steps']
        directions = [{"instruction": step['html_instructions'], "distance": step['distance']['text'], "duration": step['duration']['text']} for step in steps]
        return {"directions": directions}
    return {"error": "Impossible de trouver un itinéraire"}
