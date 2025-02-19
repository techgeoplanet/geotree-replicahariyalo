# utils.py

import requests
from django.conf import settings

def fetch_location_data(lat, lon):
    url = f"https://gpspl.geoplanetsolution.in/pincode/?lat={lat}&lon={lon}"

    headers = {
        'X-Auth-Key': 'e32ebc1d-fe04-4bd7-9003-df5274c990e2',
        'X-Username': 'shubham_gpspl'
    }

    try:
        # Make the HTTP request
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
        # Attempt to parse the response as JSON
        try:
            data = response.json()
        except ValueError as e:
            # Handle JSON decoding errors
            print(f"Error decoding JSON: {e}")
            data = {}  # Return an empty dictionary or handle as needed

        # Add lat and lon to the response data
        data.update({'lat': lat, 'lon': lon})
        return data

    except requests.RequestException as e:
        # Handle HTTP request errors (e.g., network problems, invalid URLs)
        print(f"Error making request: {e}")
        return {}  # Return an empty dictionary or handle as needed

