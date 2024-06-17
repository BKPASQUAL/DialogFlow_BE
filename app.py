from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Places with their activities
places = [
    {'name': 'Unawatuna Beach', 'latitude': 6.0041, 'longitude': 80.2505, 'activities': ['beach', 'surfing']},
    {'name': 'Hikkaduwa Beach', 'latitude': 6.1399, 'longitude': 80.1021, 'activities': ['beach', 'surfing']},
    {'name': 'Mirissa Beach', 'latitude': 5.9480, 'longitude': 80.4564, 'activities': ['beach', 'surfing']},
    {'name': 'Galle Fort', 'latitude': 6.0249, 'longitude': 80.2170, 'activities': ['sightseeing', 'history', 'walk']},
    {'name': 'Japanese Peace Pagoda', 'latitude': 6.0191, 'longitude': 80.2376, 'activities': ['sightseeing', 'photography', 'meditation']},
    {'name': 'Galle Clock Tower', 'latitude': 6.0250, 'longitude': 80.2173, 'activities': ['sightseeing', 'photography']},
    {'name': 'Galle Dutch Hospital', 'latitude': 6.0273, 'longitude': 80.2183, 'activities': ['shopping', 'dining', 'sightseeing']},
    {'name': 'Rumassala', 'latitude': 6.0011, 'longitude': 80.2707, 'activities': ['hiking', 'nature', 'sightseeing']},
    {'name': 'Hikkaduwa Coral Sanctuary', 'latitude': 6.1401, 'longitude': 80.1011, 'activities': ['snorkeling', 'diving', 'nature']},
    {'name': 'Hikkaduwa Surfing Spots', 'latitude': 6.1385, 'longitude': 80.0998, 'activities': ['surfing']},
    {'name': 'Hikkaduwa Nightclubs', 'latitude': 6.1371, 'longitude': 80.1042, 'activities': ['nightlife', 'dancing']},
    {'name': 'Unawatuna Nightclubs', 'latitude': 6.0090, 'longitude': 80.2510, 'activities': ['nightlife', 'dancing']},
    {'name': 'The Everest Futsal Court Galle', 'latitude': 6.0281, 'longitude': 80.2178, 'activities': ['sports', 'futsal']},
    {'name': 'Jungle Beach', 'latitude': 6.0063, 'longitude': 80.2460, 'activities': ['beach', 'snorkeling', 'hiking']},
    {'name': 'Koggala Lake', 'latitude': 5.9972, 'longitude': 80.3203, 'activities': ['boating', 'nature', 'bird watching']},
    {'name': 'Sea Turtle Hatchery', 'latitude': 6.0770, 'longitude': 80.1402, 'activities': ['nature', 'education']},
    {'name': 'National Maritime Museum', 'latitude': 6.0250, 'longitude': 80.2174, 'activities': ['sightseeing', 'history', 'education']},
    {'name': 'Stilt Fishermen', 'latitude': 5.9800, 'longitude': 80.3600, 'activities': ['photography', 'cultural']},
    {'name': 'Martin Wickramasinghe Folk Museum', 'latitude': 5.9706, 'longitude': 80.3465, 'activities': ['sightseeing', 'history', 'cultural']}
]

# Hotels and Villas in Hikkaduwa
accommodations = [
    {'type': 'hotel', 'name': 'Hikka Tranz by Cinnamon', 'address': 'Hikkaduwa, Sri Lanka', 'rating': 4.5},
    {'type': 'hotel', 'name': 'Coral Sands Hotel', 'address': 'Hikkaduwa, Sri Lanka', 'rating': 4.2},
    {'type': 'hotel', 'name': 'Citrus Hikkaduwa', 'address': 'Hikkaduwa, Sri Lanka', 'rating': 4.0},
    {'type': 'hotel', 'name': 'Hikkaduwa Beach Hotel', 'address': 'Hikkaduwa, Sri Lanka', 'rating': 3.8},
    {'type': 'hotel', 'name': 'Hotel Refresh Blue', 'address': 'Hikkaduwa, Sri Lanka', 'rating': 4.1},
    {'type': 'villa', 'name': 'Villa Saffron Hikkaduwa', 'address': 'Hikkaduwa, Sri Lanka', 'rating': 4.9},
    {'type': 'villa', 'name': 'Villa Shanthi', 'address': 'Hikkaduwa, Sri Lanka', 'rating': 4.8},
    {'type': 'villa', 'name': 'Villa Tara', 'address': 'Hikkaduwa, Sri Lanka', 'rating': 4.7},
    {'type': 'villa', 'name': 'Villa 46', 'address': 'Hikkaduwa, Sri Lanka', 'rating': 4.6},
    {'type': 'villa', 'name': 'Villa Birdlake', 'address': 'Hikkaduwa, Sri Lanka', 'rating': 4.5}
]

# Load historical places data
with open('places_history.json', 'r') as f:
    places_history = json.load(f)['places']

# New route to return "Hello, World!"
@app.route('/hello', methods=['GET'])
def hello_world():
    return "Hello, World!"

@app.route('/', methods=['POST'])
def webhook():
    req_data = request.get_json()
    
    # Extract intent and parameters from the request
    intent = req_data.get('queryResult').get('intent').get('displayName')
    parameters = req_data.get('queryResult').get('parameters')
    
    # Log the received data for debugging
    print(f"Received intent: {intent}")
    print(f"Received parameters: {parameters}")
    
    # Initialize response text
    response_text = ""

    # Handle "SelectActivitiesHikkaduwa" intent
    if intent == "SelectActivitiesHikkaduwa":
        selected_activities = parameters.get('Activities', [])
        recommended_places = [place for place in places if 'Hikkaduwa' in place['name'] and any(activity in place['activities'] for activity in selected_activities)]
        
        if recommended_places:
            response_text += f"Here are some places in Hikkaduwa where you can do {', '.join(selected_activities)}:\n\n"
            for place in recommended_places:
                response_text += f"{place['name']}:\n"
                response_text += f"Activities: {', '.join(place['activities'])}\n\n"
        else:
            response_text = f"Sorry, there are no places in Hikkaduwa offering {', '.join(selected_activities)}."

    # Handle "FindHotels" intent
    elif intent == "FindHotels":
        accommodation_type = parameters.get('hotelType', '').lower()
        if accommodation_type in ['hotel', 'villa']:
            filtered_accommodations = [acc for acc in accommodations if acc['type'] == accommodation_type]
            if filtered_accommodations:
                response_text += f"Here are some recommended {accommodation_type}s in Hikkaduwa:\n\n"
                for acc in filtered_accommodations:
                    response_text += f"{'Hotel' if accommodation_type == 'hotel' else 'Villa'} Name: {acc['name']}\n"
                    response_text += f"Address: {acc['address']}\n"
                    response_text += f"Rating: {acc['rating']}\n\n"
            else:
                response_text = f"Sorry, there are no {accommodation_type}s available in Hikkaduwa."
        else:
            response_text = "What kind of accommodation are you looking for: hotel or villa?"

    # Handle "SpecifyAccommodationType" intent
    elif intent == "selectHotelorVilla":
        accommodation_type = parameters.get('hotelType', '').lower()
        if accommodation_type in ['hotel', 'villa']:
            filtered_accommodations = [acc for acc in accommodations if acc['type'] == accommodation_type]
            if filtered_accommodations:
                response_text += f"Here are some recommended {accommodation_type}s in Hikkaduwa:\n\n"
                for acc in filtered_accommodations:
                    response_text += f"{'Hotel' if accommodation_type == 'hotel' else 'Villa'} Name: {acc['name']}\n"
                    response_text += f"Address: {acc['address']}\n"
                    response_text += f"Rating: {acc['rating']}\n\n"
            else:
                response_text = f"Sorry, there are no {accommodation_type}s available in Hikkaduwa."
        else:
            response_text = "Please specify whether you are looking for a hotel or a villa."

    # Handle "FindHistory" intent
    elif intent == "PlacesInGalle":
        place_name = parameters.get('places', '').title()
        found = False
        
        for place in places_history:
            if place['name'] == place_name:
                response_text += f"Here is the historical information about {place_name}:\n\n"
                response_text += place['history']
                found = True
                break
        
        if not found:
            response_text = f"Sorry, I don't have historical information about {place_name}."
    
    # Default response for other intents
    else:
        area = parameters.get('geo-city')
        activities = parameters.get('Activities')
        filtered_places = [place for place in places if area in place['name'] and any(activity in place['activities'] for activity in activities)]
        
        if filtered_places:
            response_text += f"Here are some places in {area} where you can do {', '.join(activities)}:\n\n"
            for place in filtered_places:
                response_text += f"{place['name']}:\n"
                response_text += f"Activities: {', '.join(place['activities'])}\n\n"
        else:
            response_text = f"Sorry, there are no places in {area} offering {', '.join(activities)}."

    return jsonify({'fulfillmentText': response_text})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
