import requests
import json

LATITUDE = 0.0
LONGITUDE = 0.0

def getSunTimes():
    reponse = requests.get(f"https://api.sunrise-sunset.org/json?lat={LATITUDE}&lng={LONGITUDE}")
    with open(r"C:\Users\user\Documents\Homework\Young Engineers\API\suntimes.json", "w") as f: # File is here for development purposes; not actually needed
        f.seek(0) # Allows overwriting
        json.dump(response, f, indent=4) # Dumps json file
    
