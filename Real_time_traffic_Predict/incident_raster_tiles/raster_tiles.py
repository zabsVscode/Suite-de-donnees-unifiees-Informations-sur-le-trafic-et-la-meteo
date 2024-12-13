import json
import requests
from PIL import Image
from io import BytesIO
import folium

def load_config(config_file='config.json'):
    """Load API configuration from a JSON file."""
    try:
        with open(config_file) as f:
            config = json.load(f)
    except Exception as e:
        raise ValueError(f"Error loading config file: {e}")
    
    # Validate required keys in the config
    required_keys = ['baseURL', 'versionNumber', 'style', 'zoom', 'format', 'api_key', 'latitude', 'longitude']
    for key in required_keys:
        if key not in config:
            raise KeyError(f"Missing required config key: {key}")
    
    return config

def lat_lon_to_tile(lat, lon, zoom):
    """Convert latitude and longitude to tile x and y."""
    lat_rad = lat * (3.141592653589793 / 180)
    n = 2.0 ** zoom
    x = int((lon + 180.0) / 360.0 * n)
    y = int((1.0 - (lat_rad / 3.141592653589793)) / 2.0 * n)
    return x, y

def generate_url(base_url, version, style, zoom, x, y, format, api_key, t="-1"):
    """Generate the request URL for the TomTom Traffic Incident Tiles API."""
    return (f"{base_url}/traffic/map/{version}/tile/incidents/{style}/"
            f"{zoom}/{x}/{y}.{format}?key={api_key}&t={t}")

def fetch_tile(url):
    """Fetch the traffic incident tile from the TomTom API.""" 
    response = requests.get(url)
    print(f"Response Status Code: {response.status_code}")  # Debugging line
    if response.status_code == 200:
        return response.content  # return the image data in PNG format
    else:
        return handle_error_response(response)

def handle_error_response(response):
    """Handle error responses from the TomTom API.""" 
    print(f"Error Response Content: {response.content}")  # Print the response content for debugging
    if response.headers['Content-Type'] == 'application/json':
        error_info = response.json()
        return {
            "code": error_info['detailedError']['code'],
            "message": error_info['detailedError']['message']
        }
    else:
        return {
            "code": "UNKNOWN_ERROR",
            "message": "An unknown error occurred."
        }

def save_image(image_data, filename='traffic_tile.png'):
    """Save the image data to a file."""
    try:
        image = Image.open(BytesIO(image_data))
        image.save(filename, 'PNG')
        print(f"Traffic tile saved as {filename}")
    except Exception as e:
        print(f"Error saving image: {e}")

def create_map_with_tile(latitude, longitude, tile_image_path):
    """Create a Folium map and add the traffic tile as an overlay."""
    # Create a Folium map centered at the given coordinates
    m = folium.Map(location=[latitude, longitude], zoom_start=13)
    
    # Add layers for better visualization with attribution
    folium.TileLayer(
        'CartoDB positron', 
        name='CartoDB Positron', 
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    ).add_to(m)

    folium.TileLayer(
        'OpenStreetMap', 
        name='OpenStreetMap', 
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    ).add_to(m)

    folium.TileLayer(
        'Stamen Terrain', 
        name='Terrain', 
        attr='Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under ODbL.'
    ).add_to(m)

    folium.TileLayer(
        'Stamen Toner', 
        name='Toner', 
        attr='Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under ODbL.'
    ).add_to(m)

    # Add the traffic tile as an image overlay
    folium.raster_layers.ImageOverlay(
        image=tile_image_path,
        bounds=[[latitude + 0.005, longitude - 0.005], [latitude - 0.005, longitude + 0.005]],
        opacity=0.9,  # Increased opacity for more visibility
        interactive=True,
        cross_origin=True
    ).add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    # Save the map as an HTML file
    m.save('traffic_map.html')
    print("Map with traffic overlay saved as traffic_map.html.")

def main():
    config = load_config()
    
    # Assign values from config
    base_url = config['baseURL']
    version = config['versionNumber']  # Ensure version is '4'
    style = config['style']  # Ensure style is 's0' or 's0-dark'
    zoom = int(config['zoom'])  # Convert zoom to integer
    latitude = config['latitude']
    longitude = config['longitude']
    
    # Convert latitude and longitude to tile coordinates
    x, y = lat_lon_to_tile(latitude, longitude, zoom)
    
    # Generate the URL
    url = generate_url(base_url, version, style, zoom, x, y, config['format'], config['api_key'])
    print(f"Generated URL: {url}")  # Debugging line
    
    # Fetch the tile
    tile_data = fetch_tile(url)

    if isinstance(tile_data, bytes):
        # Check if the image is not empty
        if tile_data:
            save_image(tile_data)  # Save the image
            create_map_with_tile(latitude, longitude, 'traffic_tile.png')  # Create a map with the tile overlay
        else:
            print("Error: The fetched tile data is empty.")
    else:
        print(f"Error: {tile_data['code']} - {tile_data['message']}")

if __name__ == "__main__":
    main()
