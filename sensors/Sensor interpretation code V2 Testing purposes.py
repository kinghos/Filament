#------------------------------------------Thorium - PA Pi-------------------------------------------
# Sensor code V1.5
#  - Author & Date: Umar, 2.2.22
#  - Description: Finds time wasted from sensor data & when it is wasted
#                 Will only work at night as the photodiode serves only to tell if it is light or not
#                 The daylight API should say when to pause everything and to stop recording at day.
#----------------------------------------------------------------------------------------------------


#!/usr/bin/python

# Imports
import time
import datetime
import RPi.GPIO as GPIO

# GPIO Setup
GPIO.setmode(GPIO.BOARD)

# Pin numbers
photodiode = 3 # Using PIN 3 (GPIO 2) as Input
pir = 5 # Using PIN 5 (GPIO 3) as Input

# Sets pins as digital in pins
GPIO.setup(photodiode,GPIO.IN) 
GPIO.setup(pir,GPIO.IN)

# Globals & set-up
wasted_mins = 0
interval = 2*60 # time in minutes
wasted_prev = False


while True:
    light = GPIO.input(photodiode) == 1
    motion = GPIO.input(pir) == 1
    
    wasted_condition = light and (not motion)
    # If the lights are on and there's no-one there, then it's wasted energy
    
    # Output start and end times of when energy has been wasted
    if wasted_condition and not wasted_prev: # i.e. wasted_condition has just become True
        start = datetime.datetime.now()
    elif wasted_prev: # i.e. [interval] seconds beforehand, energy was being wasted
        end = datetime.datetime.now()
    
    wasted_mins += int(wasted_condition) * interval
    
    wasted_prev = wasted_condition 
    time.sleep(interval)

