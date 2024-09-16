import googlemaps # pip install googlemaps
import requests
from flask import Flask, request, jsonify # pip install Flask

API_KEY = "AIzaSyB8y_QBXEuxLZUo4xlKs9mKb622hwlOJMw"

# Create googlemaps client object
gmaps = googlemaps.Client(key=API_KEY)

apps = Flask(__name__)

# Obtaining the latitude and longitude of Atlanta, GA
geocode_result = gmaps.geocode('Atlanta, GA')
location = geocode_result[0]['geometry']['location']
atlanta_lat_lng = (location['lat'], location['lng'])

def index():
    #initial nearest 20 results
    places_result = gmaps.places_nearby(location=atlanta_lat_lng, radius=4000, type='restaurant')
    results = [{
        'name': place['name'],
        'address': place.get('vicinity'),
        'price_level': place.get('price_level', 'N/A'),
        'rating': place.get('rating', 'N/A')
    } for place in places_result['results'][:20]]
    
    return jsonify(results)

def search():
    # Obtain user inputs and filters
    keyword = request.args.get('keyword')
    price_level = request.get.args.get('price_level')
    rating_threshold = request.args.get('rating_threshold')
    open_now = request.args.get('open_now') == 'yes'

    # Applying the search
    places_results = gmaps.places_nearby(location=atlanta_lat_lng, radius=4000, type='restaurant', keyword=keyword if keyword else None)

    # Filtered results
    filtered_results = []
    for place in places_results['results']:
        if price_level and place.get('price_level') != price_level:
            continue
        if rating_threshold and place.get('rating') < rating_threshold:
            continue
        filtered_results.append({
            'name': place['name'],
            'address': place.get('vicinity'),
            'price_level': place.get('price_level'),
            'rating': place.get('rating'),
        })

    return jsonify(filtered_results)

if __name__ == '__main__':
    apps.run(debug=True)
