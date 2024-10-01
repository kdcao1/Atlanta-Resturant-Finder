from flask import Flask, request, jsonify # pip install Flask
import googlemaps # pip install googlemaps
from flask_cors import CORS # pip install flask_cors
from dotenv import load_dotenv
load_dotenv()

# Libraries for synchronized launch
import os
import webbrowser
import threading
import subprocess
app = Flask(__name__)
CORS(app)

import math

setPort = 443

def calculate_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    km = 6371 * c
    return km

# Initialize the Google Maps client
gmaps = googlemaps.Client(key=os.getenv('GMAPS_API_KEY'))

# Get coordinates for Atlanta, GA
atlanta_lat_lng = (33.7490, -84.3880)

def get_place_details(place_id):
    # Request place details from the Google Maps API
    details_result = gmaps.place(place_id=place_id, fields=[
        'formatted_phone_number', 'website', 'opening_hours', 'delivery', 
        'wheelchair_accessible_entrance', 'curbside_pickup', 'dine_in',
        'editorial_summary', 'price_level', 'rating', 'reservable',
        'reviews', 'serves_beer', 'serves_breakfast', 'serves_brunch',
        'serves_dinner', 'serves_lunch', 'serves_vegetarian_food',
        'serves_wine', 'takeout', 'user_ratings_total'
    ])
    return details_result.get('result', {})

# Function to get places from Google Maps API
def get_places(lat_lng, radius=18000, keyword=None, open_now=None, price_level=None, rating_threshold=None):
    # Call the Google Maps API
    places_result = gmaps.places_nearby(
        location=lat_lng,
        radius=radius,
        type='restaurant',
        keyword=keyword if keyword else None,
        open_now=open_now
    )

    # Filter by price level and rating, if provided
    filtered_places = []
    for place in places_result['results']:
        place_id = place.get('place_id')
        if place_id:
            details = get_place_details(place_id)
            distance = calculate_distance(
                atlanta_lat_lng[0], atlanta_lat_lng[1],
                place['geometry']['location']['lat'], place['geometry']['location']['lng']
            )
            filtered_places.append({
                'name': place['name'],
                'address': place.get('vicinity'),
                'price_level': place.get('price_level', 'N/A'),
                'rating': place.get('rating', 'N/A'),
                'distance': distance,
                'status': place.get('opening_hours', False),
                'id': place.get('place_id'),
                'coords': place.get('geometry'),
                'phone_number': details.get('formatted_phone_number', 'N/A'),
                'website': details.get('website', 'N/A'),
                'opening_hours': details.get('opening_hours', {}).get('weekday_text', []),
                'curbside_pickup': details.get('curbside_pickup', False),
                'delivery': details.get('delivery', False),
                'dine_in': details.get('dine_in', False),
                'editorial_summary': details.get('editorial_summary', {}).get('overview', ''),
                'reservable': details.get('reservable', False),
                'reviews': details.get('reviews', []),
                'serves_beer': details.get('serves_beer', False),
                'serves_breakfast': details.get('serves_breakfast', False),
                'serves_brunch': details.get('serves_brunch', False),
                'serves_dinner': details.get('serves_dinner', False),
                'serves_lunch': details.get('serves_lunch', False),
                'serves_vegetarian_food': details.get('serves_vegetarian_food', False),
                'serves_wine': details.get('serves_wine', False),
                'takeout': details.get('takeout', False),
                'user_ratings_total': details.get('user_ratings_total', 0),
            })
            
    # Test print to verify that the restaurants are being fetched correctly
    print("Fetched Restaurants:")
    for place in filtered_places:
        print(place['name'])

    # Return the filtered list (limit to 20 results)
    return filtered_places[:20]

# Route to get the initial 20 locations
@app.route('/initial', methods=['GET'])
def initial_load():
    places = get_places(atlanta_lat_lng)
    return jsonify({'places': places})

# Route to get the updated 20 locations based on user preferences
@app.route('/search', methods=['POST'])
def search():
    # Get the user preferences from the request
    data = request.get_json()
    keyword = data.get('keyword')
    
    # Fetch the places with the updated preferences
    places = get_places(
        lat_lng=atlanta_lat_lng,
        keyword=keyword
    )

    # Return the new results
    return jsonify({'places': places})

# Function to open the browser
def open_browser():
    webbrowser.open('http://127.0.0.1:'+str(setPort)+'/initial')

# Path to manage.py directory
def run_django_server():

    # BEFORE RUNNING, REMEMBER TO CHANGE THE PATH TO THE DIRECTORY WHERE manage.py IS LOCATED LOCALLY
    manage_py_dir = r'C:\Users\Brian\Desktop\CompSci\CS2340\Atlanta-Resturant-Finder\Atlanta_Food_Finder'
    
    # Run manage.py runserver using subprocess
    subprocess.run(['python', 'manage.py', 'runserver'], cwd=manage_py_dir, check=True)


if __name__ == '__main__':
    # Only open the browser if not in reloader mode to not make it run twice
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        threading.Timer(1.25, open_browser).start()
        threading.Timer(1.5, run_django_server).start()  # Run Django server slightly after opening the browser

    app.run(host='127.0.0.1', port=setPort, debug=True)