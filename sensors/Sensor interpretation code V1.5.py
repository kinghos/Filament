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

# Globals & set-up
wasted_mins = 0
interval = 2*60 # time in minutes
wasted_prev = False

# Pin numbers - change when connected
photodiode_50 = 3 # Filtered ~50Hz signal
pir = 4

# NB: No need for photodiode to be connected 

GPIO.setmode(GPIO.BCM) # Not sure
GPIO.setwarnings(False) # Not sure

# Sets pins as digital in pins
GPIO.setup(photodiode_50,GPIO.IN) 
GPIO.setup(pir,GPIO.IN) 

def daylight():
    return True # Need this to link to Kingshuk's light_monitoring API code


while True:
    artificial_light = GPIO.input(photodiode_filtered)
    natural_light = daylight()
    motion = GPIO.input(pir) == 1
    
    wasted_condition = (artificial_light and not motion) or (natural_light and artificial_light)
    # If the lights are on and there's no-one there, then it's wasted energy
    # If the lights are on and it's daytime, then it's also wasted energy
    
    # Output start and end times of when energy has been wasted
    if wasted_condition and not wasted_prev: # i.e. wasted_condition has just become True
        start = datetime.datetime.now()
        print(start)
    elif wasted_prev: # i.e. [interval] seconds beforehand, energy was being wasted
        end = datetime.datetime.now()
    
    wasted_mins += int(wasted_condition) * interval
    
    wasted_prev = wasted_condition 
    time.sleep(interval)
