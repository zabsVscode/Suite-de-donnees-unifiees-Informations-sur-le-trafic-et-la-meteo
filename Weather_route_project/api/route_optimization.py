import requests

def optimize_routes(locations):
    API_KEY = 'TON_API_KEY_GOOGLE'
    url = f"https://routes.googleapis.com/v1/optimize?locations={locations}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data.get('optimizedRoute'):
        return {"optimizedRoute": data['optimizedRoute']}
    return {"error": "Impossible d'optimiser l'itinéraire"}
