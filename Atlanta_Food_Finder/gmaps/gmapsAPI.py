import googlemaps # pip install googlemaps
import requests
from flask import Flask, request, jsonify # pip install Flask
import os
from dotenv import load_dotenv
load_dotenv()

# Create googlemaps client object
gmaps = googlemaps.Client(key=os.getenv('GMAPS_API_KEY'))

apps = Flask(__name__)

# some location stuff
geocode_result = gmaps.geocode('Atlanta, GA')
location = geocode_result[0]['geometry']['location']
atlanta_lat_lng = (33.7490, -84.3880)

# Main function to get places
def get_places(atlanta_lat_lng, radius=5000, keyword=None, open_now=None, price_level=None, rating_threshold=None, page_token=None):
    # Call the Google Maps API
    places_result = gmaps.places_nearby(
        location=atlanta_lat_lng,
        radius=radius,
        type='restaurant',
        keyword=keyword if keyword else None,
        open_now=open_now,
        page_token=page_token
    )

    # filtered places if filtered
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
            'rating': place.get('rating', 'N/A')
        })

    # Return the filtered results
    return filtered_places[:20]


# Self explanatory
def initial_load():
    places = get_places(atlanta_lat_lng)
    return jsonify({'places': places})

# Search function
def search():
    # Get the user preferences from the request
    data = request.get_json()
    keyword = data.get('keyword')
    price_level = data.get('price_level')
    rating_threshold = data.get('rating_threshold')
    open_now = data.get('open_now')

    # Fetch places with updated prefs
    places = get_places(
        lat_lng=atlanta_lat_lng,
        keyword=keyword,
        open_now=open_now,
        price_level=price_level,
        rating_threshold=rating_threshold
    )

    # Return mew results
    return jsonify({'places': places})

if __name__ == '__main__':
    apps.run(debug=True)







# def index():
#     #initial nearest 20 results
#     places_result = gmaps.places_nearby(location=atlanta_lat_lng, radius=4000, type='restaurant')
#     results = [{
#         'name': place['name'],
#         'address': place.get('vicinity'),
#         'price_level': place.get('price_level', 'N/A'),
#         'rating': place.get('rating', 'N/A')
#     } for place in places_result['results'][:20]]
    
#     return jsonify(results)

# def search():
#     # Obtain user inputs and filters
#     keyword = request.args.get('keyword')
#     price_level = request.get.args.get('price_level')
#     rating_threshold = request.args.get('rating_threshold')
#     open_now = request.args.get('open_now') == 'yes'

#     # Applying the search
#     places_results = gmaps.places_nearby(location=atlanta_lat_lng, radius=4000, type='restaurant', keyword=keyword if keyword else None)

#     # Filtered results
#     filtered_results = []
#     for place in places_results['results']:
#         if price_level and place.get('price_level') != price_level:
#             continue
#         if rating_threshold and place.get('rating') < rating_threshold:
#             continue
#         filtered_results.append({
#             'name': place['name'],
#             'address': place.get('vicinity'),
#             'price_level': place.get('price_level'),
#             'rating': place.get('rating'),
#         })

#     return jsonify(filtered_results)

# if __name__ == '__main__':
#     apps.run(debug=True)
