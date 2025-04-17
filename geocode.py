import os
import requests

def get_coordinates(address):
    if not GOOGLE_MAPS_API_KEY:
        print("Missing Google Maps API Key")
        return None, None

    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key=AIzaSyBQ_Tps_6uIvQAvKH5LtVVP9U99N3gVCaE"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    
    return None, None
