import requests

def get_roads(path):
    API_KEY = 'API_KEY_GOOGLE'
    url = f"https://roads.googleapis.com/v1/snapToRoads?path={path}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data.get('snappedPoints'):
        return {"roads": data['snappedPoints']}
    return {"error": "Impossible d'identifier les routes"}
