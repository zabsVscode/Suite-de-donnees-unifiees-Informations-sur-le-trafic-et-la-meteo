import requests

def get_route(start, end):
    API_KEY = 'TON_API_KEY_GOOGLE'
    url = f"https://routes.googleapis.com/maps/api/directions/json?origin={start}&destination={end}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'OK':
        route = data['routes'][0]
        return {"route": route['summary'], "legs": route['legs']}
    return {"error": "Impossible de trouver la route"}
