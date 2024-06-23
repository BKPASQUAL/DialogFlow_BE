from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load data from JSON files
with open('places.json', 'r') as f:
    places = json.load(f)['places']

with open('accommodations.json', 'r') as f:
    accommodations = json.load(f)['accommodations']

with open('places_history.json', 'r') as f:
    places_history = json.load(f)['places']

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
    # elif intent == "FindHotels":
    #     accommodation_type = parameters.get('hotelType', '').lower()
    #     hotel_place = parameters.get('hotelplace', '').lower()
    #     if accommodation_type in ['hotel', 'villa']:
    #         if hotel_place in ['beachside', 'without beachside']:
    #             location_filter = 'beachside' if hotel_place == 'beachside' else 'without beachside'
    #             filtered_accommodations = [acc for acc in accommodations if acc['type'] == accommodation_type and acc['location'] == location_filter]
    #             if filtered_accommodations:
    #                 response_text += f"Here are some recommended {accommodation_type}s in Hikkaduwa ({hotel_place}):\n\n"
    #                 for acc in filtered_accommodations:
    #                     response_text += f"{'Hotel' if accommodation_type == 'hotel' else 'Villa'} Name: {acc['name']}\n"
    #                     response_text += f"Address: {acc['address']}\n"
    #                     response_text += f"Rating: {acc['rating']}\n\n"
    #             else:
    #                 response_text = f"Sorry, there are no {accommodation_type}s available in Hikkaduwa ({hotel_place})."
    #         else:
    #             response_text = "Please specify if you want a beachside or without beachside accommodation."
    #     else:
    #         response_text = "What kind of accommodation are you looking for: hotel or villa?"

    # Handle "SelectBeachHotelInHikkaduwa" intent
    elif intent == "SelectBeachHotelInHikkaduwa":
        filtered_accommodations = [acc for acc in accommodations if acc['type'] == 'hotel' and acc['location'] == 'beachside']
        if filtered_accommodations:
            response_text += f"Here are some recommended beachside hotels in Hikkaduwa:\n\n"
            for acc in filtered_accommodations:
                response_text += f"Hotel Name: {acc['name']}\n"
                response_text += f"Address: {acc['address']}\n"
                response_text += f"Rating: {acc['rating']}\n\n"
        else:
            response_text = "Sorry, there are no beachside hotels available in Hikkaduwa."

    # Handle "SpecifyAccommodationType" intent
    # elif intent == "SpecifyAccommodationType":
    #     accommodation_type = parameters.get('hotelType', '').lower()
    #     if accommodation_type in ['hotel', 'villa']:
    #         filtered_accommodations = [acc for acc in accommodations if acc['type'] == accommodation_type]
    #         if filtered_accommodations:
    #             response_text += f"Here are some recommended {accommodation_type}s in Hikkaduwa:\n\n"
    #             for acc in filtered_accommodations:
    #                 response_text += f"{'Hotel' if accommodation_type == 'hotel' else 'Villa'} Name: {acc['name']}\n"
    #                 response_text += f"Address: {acc['address']}\n"
    #                 response_text += f"Rating: {acc['rating']}\n\n"
    #         else:
    #             response_text = f"Sorry, there are no {accommodation_type}s available in Hikkaduwa."
    #     else:
    #         response_text = "Please specify whether you are looking for a hotel or a villa."

    # Handle "HistoricalPlaces" intent
    elif intent == "HistoricalPlaces":
        city = parameters.get('city', '').lower()
        recommended_places = [place for place in places_history if city in place['location'].lower()]
        
        if recommended_places:
            response_text += f"Here are some historical places in {city.capitalize()}:\n\n"
            for place in recommended_places:
                response_text += f"{place['name']}:\n"
                response_text += f"Description: {place['description']}\n"
                response_text += f"Location: {place['location']}\n\n"
        else:
            response_text = f"Sorry, there are no historical places listed in {city.capitalize()}."

    # Handle unrecognized intent
    else:
        response_text = "Sorry, I didn't understand that request."

    # Log the response for debugging
    print(f"Response text: {response_text}")
    
    # Return the response text
    return jsonify({'fulfillmentText': response_text})

if __name__ == '__main__':
    app.run(debug=True)
