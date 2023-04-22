import requests
import json
import datetime

LATITUDE = 51.5072
LONGITUDE = -0.1276

def getSunTimes():
    response = requests.get(f"https://api.sunrise-sunset.org/json?lat={LATITUDE}&lng={LONGITUDE}")
    response = response.json()

    with open("sunTimes.json", "w") as f: # File is here for development purposes; not actually needed
        f.seek(0) # Allows overwriting
        json.dump(response, f, indent=4) # Dumps json file
    
    sunrise = datetime.datetime.strptime(response["results"]["sunrise"], "%H:%M:%S %p")
    sunset = datetime.datetime.strptime(response["results"]["sunset"], "%H:%M:%S %p")

    now = datetime.datetime.now(datetime.timezone.utc)
    if now.astimezone(datetime.timezone(datetime.timedelta(hours=1))).strftime('%z') == '+0100':
        sunrise += datetime.timedelta(hours=1)
        sunset += datetime.timedelta(hours=13)

    now = datetime.datetime.now().time()
    return sunrise.time() < now < sunset.time()
 
print(getSunTimes())