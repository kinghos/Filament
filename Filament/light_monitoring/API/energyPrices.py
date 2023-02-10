#------------------------------------------Thorium - PA Pi-------------------------------------------
# Energy price calculation code
#  - Author & Date: Kingshuk, 14.1.22
#  - Description: Grabs data on energy prices
#    Takes the nearest 30 min period of the day, and then obtains the previous day's data at that time
#----------------------------------------------------------------------------------------------------


import requests
import json
from datetime import datetime, timedelta


END_DATE = datetime.now() 
START_DATE = END_DATE - timedelta(days=1)
END_DATE = END_DATE.strftime("%d-%m-%Y")
START_DATE = START_DATE.strftime("%d-%m-%Y")

DNO = 12 # Regional code - defaults to 12 (London)
VOLTAGE = "LV"
HEADERS = {
    'Accept':'application/json'
}


def roundTime(date):
    minute = date.minute
    if minute < 15:
        date = date.replace(minute=0, second=0, microsecond=0)
    elif minute >= 15  and minute < 45:
        date = date.replace(minute=30, second=0, microsecond=0)
    elif minute >= 45:
        date = date.replace(minute=0, second=0, microsecond=0)
        date += timedelta(hours=1)
    return date


def getEnergyCosts(DNO):
    response = requests.get(f"https://odegdcpnma.execute-api.eu-west-2.amazonaws.com/development/prices?dno={DNO}&voltage={VOLTAGE}&start={START_DATE}&end={END_DATE}", params={}, headers = HEADERS) # Gets the json from the url
    priceDict = response.json()

    with open("energyPrices.json", "w") as f: # File is here for development purposes; not actually needed
        f.seek(0) # Allows overwriting
        json.dump(priceDict, f, indent=4) # Dumps json file
    
    timeList = []
    for dic in priceDict["data"]["data"]:
        timeList.append(dic["Timestamp"])

    index = -1
    roundNow = roundTime(datetime.now() - timedelta(days=1)).strftime("%H:%M %d-%m-%Y")
    for i in range(len(timeList)):
        if str(timeList[i]) == roundNow:
            index = i

    return float(priceDict["data"]["data"][index]["Overall"]) # Returns the price. The price taken is the closest time from the previous day's data
    
def calcPrices(power, time, numBulbs, prices): # Takes power in watts and time in hours
    power /= 1000 # Converts W to kW
    return power * time * numBulbs * prices

# At the time this is called, the price from the nearest time the previous day is returned
# energyCosts = getEnergyCosts(DNO)
# print(f"Energy costs: £{energyCosts}/kWh")
# print(f"Cost of usage: £{calcPrices(50, 1, 1, energyCosts):.2f} today")
