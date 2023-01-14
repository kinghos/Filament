import requests
import json

START_DATE = "13-01-2023"
END_DATE = "14-01-2023"
DNO = 12 # Regional code - defaults to 12 (London)
VOLTAGE = "LV"
api_url = f"https://odegdcpnma.execute-api.eu-west-2.amazonaws.com/development/prices?dno={DNO}&voltage={VOLTAGE}&start={START_DATE}&end={START_DATE}"

with requests.Session() as s: # Starts a request session
    response = s.get(api_url).text # Gets the json from the url

response_info = json.loads(response) # Loads json into a dictionary
print(response_info)
with open("data.json", "w") as f:
    json.dump(response_info, f, indent=4) # Dumps json file 