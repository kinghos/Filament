#------------------------------------------Thorium - PA Pi-------------------------------------------
# Sensor code for SYS-V2
#  - Author & Date: Umar and Kingshuk (for daylight func and Django interfacing)
#  - Description: Finds time wasted from sensor data & when it is wasted
#----------------------------------------------------------------------------------------------------

#!/usr/bin/python

# Imports
import time
import datetime
import RPi.GPIO as GPIO
import django
from django.conf import settings
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent.parent
if not settings.configured:
    settings.configure(DATABASES= {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }})
        
django.setup()

from models import Data_Entry


# Pin numbers
system = 3 # Using PIN 3 (GPIO 2) as Input
pir = 5 # Using PIN 5 (GPIO 3) as Input

# GPIO Setup
GPIO.setmode(GPIO.BOARD)

# Sets pins as digital in pins
GPIO.setup(system,GPIO.IN) 
GPIO.setup(pir,GPIO.IN) 


# Globals & set-up
interval = 2 # seconds
is_wasted_prev = False
LATITUDE = 51.5072
LONGITUDE = -0.1276

def daylight():
    response = requests.get(f"https://api.sunrise-sunset.org/json?lat={LATITUDE}&lng={LONGITUDE}")
    response = response.json()

    sunrise = datetime.datetime.strptime(response["results"]["sunrise"], "%H:%M:%S %p")
    sunset = datetime.datetime.strptime(response["results"]["sunset"], "%H:%M:%S %p")

    now = datetime.datetime.now(datetime.timezone.utc)
    if now.astimezone(datetime.timezone(datetime.timedelta(hours=1))).strftime('%z') == '+0100':
        sunrise += datetime.timedelta(hours=1)
        sunset += datetime.timedelta(hours=13)

    now = datetime.datetime.now().time()
    return (sunrise + datetime.timedelta(hours = 2)).time() < now < (sunset - datetime.timedelta(hours = 2)).time()



while True:
    out_system = bool(GPIO.input(system))
    motion = bool(GPIO.input(pir))
    natural_light = daylight() # Link to sunset/sunrise API
    
    # If over the period of 0.5 seconds, the system outputs a 1 at least once, artificial light is true, else it is false
    artificial_light = False
    for i in range(500):
        out_system = bool(GPIO.input(system))
        if out_system:
            artificial_light = True
        time.sleep(0.001)
     
    is_wasted = (artificial_light and not motion) or (natural_light and artificial_light)
    
    # Output start and end times of when energy has been wasted
    if is_wasted and not is_wasted_prev: # i.e. wasted_condition has just become True
        start = datetime.datetime.now()
        
    elif is_wasted_prev: # i.e. <interval> seconds beforehand, energy was being wasted
        end = datetime.datetime.now()
        newEntry = Data_Entry(startTime=start, endTime=end)
        newEntry.save()
      
    is_wasted_prev = is_wasted # Records whether energy was wasted last reading
    print('is_wasted: ', is_wasted)
    time.sleep(interval)
