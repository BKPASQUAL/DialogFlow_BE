from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load data from JSON files
with open('places.json', 'r') as f:
    places = json.load(f)['places']

with open('places_history.json', 'r') as f:
    places_history = json.load(f)['placesInGalle']

with open('accommodations.json', 'r') as f:
    accommodations_data = json.load(f)
    accommodations_hikkaduwa = accommodations_data['Hikkaduwa Hotels']
    accommodations_galle = accommodations_data['Galle Hotels']

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

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
        recommended_places = [
            place for place in places if 'Hikkaduwa' in place['name'] and
            any(activity in place['activities'] for activity in selected_activities)
        ]

        if recommended_places:
            response_text += f"Here are some places in Hikkaduwa where you can do {', '.join(selected_activities)}:\n\n"
            for place in recommended_places:
                response_text += f"{place['name']}:\n"
                response_text += f"Activities: {', '.join(place['activities'])}\n\n"
        else:
            response_text = f"Sorry, there are no places in Hikkaduwa offering {', '.join(selected_activities)}."

    # Handle "SelectBeachHotelInHikkaduwa" intent
    elif intent == "SelectBeachHotelInHikkaduwa":
        location_preference = parameters.get('hotelplace', '').lower()
        filtered_accommodations = []

        if "beachside" in location_preference:
            filtered_accommodations = [
                acc for acc in accommodations_hikkaduwa if acc['type'] == 'hotel' and acc.get('location') == 'beachside'
            ]
            response_text += "Here are some recommended beachside hotels in Hikkaduwa:\n\n"
        elif "without beach" in location_preference:
            filtered_accommodations = [
                acc for acc in accommodations_hikkaduwa if acc['type'] == 'hotel' and acc.get('location') != 'beachside'
            ]
            response_text += "Here are some recommended hotels in Hikkaduwa (without beachside):\n\n"
        else:
            response_text = "Please specify whether you want 'beachside' or 'without beach' hotels."

        if filtered_accommodations:
            for acc in filtered_accommodations:
                response_text += f"Hotel Name: {acc['name']}\n"
                response_text += f"Address: {acc['address']}\n"
                response_text += f"Rating: {acc['rating']}\n"
                response_text += f"Location: {acc['location']}\n\n"
        else:
            response_text = "Sorry, there are no hotels available in Hikkaduwa based on your preference."

    # Handle "SelectVillaInHikkaduwa" intent
    elif intent == "SelectVillaInHikkaduwa":
        villa_place = parameters.get('VillaPlace', '').lower()
        filtered_villas = []

        if "beachside" in villa_place:
            filtered_villas = [
                acc for acc in accommodations_hikkaduwa if acc['type'] == 'villa' and acc.get('location') == 'beachside'
            ]
            response_text += "Here are some recommended beachside villas in Hikkaduwa:\n\n"
        elif "without beach" in villa_place:
            filtered_villas = [
                acc for acc in accommodations_hikkaduwa if acc['type'] == 'villa' and acc.get('location') != 'beachside'
            ]
            response_text += "Here are some recommended villas in Hikkaduwa (without beachside):\n\n"
        else:
            response_text = "Please specify whether you want 'beachside' or 'without beach' villas."

        if filtered_villas:
            for acc in filtered_villas:
                response_text += f"Villa Name: {acc['name']}\n"
                response_text += f"Address: {acc['address']}\n"
                response_text += f"Rating: {acc['rating']}\n"
                response_text += f"Location: {acc['location']}\n\n"
        else:
            response_text = "Sorry, there are no villas available in Hikkaduwa based on your preference."

   # Handle "SelectBeachHotelInGAlle" intent
    elif intent == "SelectBeachHotelInGAlle":
        location_preference = parameters.get('hotelPlace', '').lower()
        if "beachside" in location_preference:
            filtered_accommodations = [
                acc for acc in accommodations_galle if acc['type'] == 'hotel' and acc.get('location') == 'beachside'
            ]
            response_text += "Here are some recommended beachside hotels in Galle:\n\n"
        else:
            filtered_accommodations = [
                acc for acc in accommodations_galle if acc['type'] == 'hotel' and acc.get('location') != 'beachside'
            ]
            response_text += "Here are some recommended hotels in Galle (without beachside):\n\n"

        if filtered_accommodations:
            for acc in filtered_accommodations:
                response_text += f"Hotel Name: {acc['name']}\n"
                response_text += f"Address: {acc['address']}\n"
                response_text += f"Rating: {acc['rating']}\n"
                response_text += f"Location: {acc['location']}\n\n"
        else:
            response_text = "Sorry, there are no hotels available in Galle based on your preference."


    # Handle "PlacesInGalle" intent
    elif intent == "PlacesInGalle":
        place_name = parameters.get('places', '').lower()
        recommended_places = [
            place for place in places_history if place_name in place['name'].lower()
        ]

        if recommended_places:
            response_text += f"Here are some historical places in {place_name.capitalize()}:\n\n"
            for place in recommended_places:
                response_text += f"{place['name']}:\n"
                response_text += f"History: {place['history']}\n\n"
        else:
            response_text = f"Sorry, there are no historical places listed for {place_name.capitalize()}."

    # Log the response for debugging
    print(f"Response text: {response_text}")

    # Return the response text
    return jsonify({'fulfillmentText': response_text})

if __name__ == '__main__':
    app.run(debug=True)
