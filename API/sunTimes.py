import requests
import json

LATITUDE = 0.0
LONGITUDE = 0.0

def getSunTimes():
    response = requests.get(f"https://api.sunrise-sunset.org/json?lat={LATITUDE}&lng={LONGITUDE}")
    response = response.json()

    with open("sunTimes.json", "w") as f: # File is here for development purposes; not actually needed
        f.seek(0) # Allows overwriting
        json.dump(response, f, indent=4) # Dumps json file
    
    return response["results"]["sunrise"], response["results"]["sunset"]

sunrise, sunset = getSunTimes()   
print(f"Sunrise: {sunrise}\nSunset: {sunset}")