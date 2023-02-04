#------------------------------------------Thorium - PA Pi----------------------------------------------
#    Carbon emissions calculation code
#  - Author & Date: Kingshuk, 15.1.22
#  - Description: Grabs data on carbon emissions
#    Obtains the gCO₂/kWh rates, and calculates the g of CO₂ produced by the energy used to power bulbs
#-------------------------------------------------------------------------------------------------------

import requests
import json

headers = {
  'Accept': 'application/json'
}

def getEmissionsRate():
    response = requests.get('https://api.carbonintensity.org.uk/intensity', params={}, headers = headers)
    emissionsDict = response.json()

    with open("emissions.json", "w") as f: # File is here for development purposes; not actually needed
        f.seek(0) # Allows overwriting
        json.dump(emissionsDict, f, indent=4) # Dumps json file
    
    val = emissionsDict["data"][0]["intensity"]["actual"]
    return val if val != None else emissionsDict["data"][0]["intensity"]["forecast"]

def getEmissions(power, numBulbs, time, emissions):
    power /= 1000
    return power * numBulbs * time * emissions

# emissionRate = getEmissionsRate()
# print(f"{emissionRate}gCO₂/kWh")
# print(f"{getEmissions(50, 1, 1, emissionRate)}g of CO₂")