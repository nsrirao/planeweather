import requests
import json

def getWeather(latitude = 35.8778, longitude = -78.7875, service = "weather") :
    """getWeather: Gets the weather data from a web service. 
    It requires the following parameters as inputs:
        latitude: The latitude of the place; -90 to +90 for south pole to north pole.
                    The default is for RDU.
        longitude: -180 to +180
        service: Can be any of "weather" or "forecast"
    """
    keyid = "0d07fefdfd37c8a225916bf1ac394cc0"
    url = "http://api.openweathermap.org/data/2.5/"


    url += service

    payload = {
        "APPID":  keyid,
        "lon": longitude,
        "lat":  latitude,
        "units": "metric"
        }
    headers = {"content-type": "application/json"}

    r = requests.get(url, headers=headers, params=payload)

    fdata = r.json()
    data = {
        "name": fdata.get("name"),
        "country": fdata["sys"]["country"],
        "latitude": fdata["coord"]["lat"],
        "longitude": fdata["coord"]["lon"],
        "temp": fdata["main"]["temp"],
        "humidity": fdata["main"]["humidity"],
        "wind": fdata["wind"],
        }
    return data


