import requests

def geocode_address(address):
    API_KEY = 'TON_API_KEY_GOOGLE'
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'OK':
        result = data['results'][0]
        return {
            "latitude": result['geometry']['location']['lat'],
            "longitude": result['geometry']['location']['lng']
        }
    return {"error": "Adresse introuvable"}
