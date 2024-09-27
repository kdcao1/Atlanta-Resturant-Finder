from flask import Flask, request, jsonify # pip install Flask
import googlemaps # pip install googlemaps
from flask_cors import CORS # pip install flask_cors

app = Flask(__name__)
CORS(app)

# Initialize the Google Maps client
API_KEY = 'AIzaSyB8y_QBXEuxLZUo4xlKs9mKb622hwlOJMw'
gmaps = googlemaps.Client(key=API_KEY)

# Get coordinates for Atlanta, GA
atlanta_lat_lng = (33.7490, -84.3880)

# Function to get places from Google Maps API
def get_places(lat_lng, radius=5000, keyword=None, open_now=None, price_level=None, rating_threshold=None):
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
        if price_level and place.get('price_level') != int(price_level):
            continue
        if rating_threshold and place.get('rating') < float(rating_threshold):
            continue
        filtered_places.append({
            'name': place['name'],
            'address': place.get('vicinity'),
            'price_level': place.get('price_level', 'N/A'),
            'rating': place.get('rating', 'N/A'),
            'status': place.get('opening_hours'),
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, debug=True)

# To access server after running and loading the pulls, go to http://127.0.0.1:5000/initial