from flask import Flask, jsonify, request
from geocoding import geocode_address
from directions import get_directions
from routes import get_route
from roads import get_roads
from distance_matrix import get_distance_matrix
from route_optimization import optimize_routes

app = Flask(__name__)

@app.route('/')
def hello():
    return "Bienvenue sur l'API de géolocalisation et d'itinéraires !"

# Route Geocoding (convertir une adresse en coordonnées)
@app.route('/geocode', methods=['GET'])
def geocode():
    address = request.args.get('address', '')
    if address:
        result = geocode_address(address)
        return jsonify(result)
    return jsonify({"error": "Adresse manquante"}), 400

# Route Directions (itinéraire entre deux points)
@app.route('/directions', methods=['GET'])
def directions():
    origin = request.args.get('origin', '')
    destination = request.args.get('destination', '')
    if origin and destination:
        result = get_directions(origin, destination)
        return jsonify(result)
    return jsonify({"error": "Origine ou destination manquante"}), 400

# Route Routes (données sur un itinéraire avec optimisations)
@app.route('/routes', methods=['GET'])
def route():
    start = request.args.get('start', '')
    end = request.args.get('end', '')
    if start and end:
        result = get_route(start, end)
        return jsonify(result)
    return jsonify({"error": "Point de départ ou d'arrivée manquant"}), 400

# Route Roads (identifier les routes empruntées)
@app.route('/roads', methods=['GET'])
def roads():
    path = request.args.get('path', '')
    if path:
        result = get_roads(path)
        return jsonify(result)
    return jsonify({"error": "Chemin manquant"}), 400

# Route Distance Matrix (distance et temps de trajet entre plusieurs points)
@app.route('/distance_matrix', methods=['GET'])
def distance_matrix():
    origins = request.args.get('origins', '')
    destinations = request.args.get('destinations', '')
    if origins and destinations:
        result = get_distance_matrix(origins, destinations)
        return jsonify(result)
    return jsonify({"error": "Origines ou destinations manquantes"}), 400

# Route Route Optimization (optimisation des itinéraires pour plusieurs véhicules)
@app.route('/route_optimization', methods=['GET'])
def route_optimization():
    locations = request.args.get('locations', '')
    if locations:
        result = optimize_routes(locations)
        return jsonify(result)
    return jsonify({"error": "Localisations manquantes"}), 400

if __name__ == "__main__":
    app.run(debug=True)
