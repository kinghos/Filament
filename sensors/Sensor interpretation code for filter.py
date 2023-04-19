#------------------------------------------Thorium - PA Pi-------------------------------------------
# Sensor code V1.5
#  - Author & Date: Umar, 2.2.22
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

BASE_DIR = Path(__file__).resolve().parent.parent
if not settings.configured:
    settings.configure(DATABASES= {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }})
        
django.setup()

from Filament.light_monitoring.models import Data_Entry


# Pin numbers
system = 3 # Filtered signal from circuit
pir = 4

# GPIO Setup
GPIO.setmode(GPIO.BOARD)

# Sets pins as digital in pins
GPIO.setup(system,GPIO.IN) 
GPIO.setup(pir,GPIO.IN) 


# Globals & set-up
wasted_mins = 0
interval = 120 # seconds
wasted_prev = False


def daylight():
    return True # Need this to link to Kingshuk's light_monitoring API code



while True:
    system_light = bool(GPIO.input(system))
    motion = bool(GPIO.input(pir))
    natural_light = daylight() # link to API
    
    # Artificial light is true unless the system has outputted 0 for 2 seconds
    artificial_light = True
    no_system_light_count = 0
    while not(system_light):
        time.sleep(0.25)
        no_system_light_count += 1
        if no_system_light_count > 8: # If the system has outputted 0 continuously for 0.25 * 8 = 2 seconds 
            artificial_light = False
    
    wasted_condition = (artificial_light and not motion) or (natural_light and artificial_light)
    # If the lights are on and there's no-one there, then it's wasted energy
    # If the lights are on and it's daytime, then it's also wasted energy
    
    # Output start and end times of when energy has been wasted
    if wasted_condition and not wasted_prev: # i.e. wasted_condition has just become True
        start = datetime.datetime.now()
        
    elif wasted_prev: # i.e. [interval] seconds beforehand, energy was being wasted
        end = datetime.datetime.now()
        newEntry = Data_Entry(startTime=start, endTime=end)
        newEntry.save()
    
    wasted_mins += int(wasted_condition) * interval
    
    wasted_prev = wasted_condition 
    time.sleep(interval)
