import requests
import json
import datetime

headers = {
  'Accept': 'application/json'
}
 
response = requests.get('https://api.carbonintensity.org.uk/intensity', params={}, headers = headers)

with open(r"C:\Users\user\Documents\Homework\Young Engineers\API\emissions.json", "w") as f: # File is here for development purposes; not actually needed
    f.seek(0) # Allows overwriting
    json.dump(response, f, indent=4) # Dumps json file
