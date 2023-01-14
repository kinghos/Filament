import requests
import json

START_DATE = "12-01-2023"
END_DATE = "14-01-2023"
DNO = 12 # Regional code - defaults to 12 (London)
VOLTAGE = "LV"
headers = {
    'Accept':'application/json'
}
api_url = f"https://odegdcpnma.execute-api.eu-west-2.amazonaws.com/development/prices?dno={DNO}&voltage={VOLTAGE}&start={START_DATE}&end={END_DATE}"

response = requests.get(api_url, params={}, headers=headers) # Gets the json from the url

with open(r"C:\Users\user\Documents\Homework\Young Engineers\API\energyPrices.json", "w") as f:
    json.dump(response.json(), f, indent=4) # Dumps json file