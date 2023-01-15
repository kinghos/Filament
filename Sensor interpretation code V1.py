#------------------------------------------Thorium - PA Pi-------------------------------------------
# Sensor code V1
#  - Author & Date: Umar, 15.1.22
#  - Description: A test using the light levels, UV levels, and motion.
#                 Functions are incomplete.
#----------------------------------------------------------------------------------------------------


#!/usr/bin/python

# Imports
import time
import RPi.GPIO as GPIO

# Globals & set-up
wasted_mins = 0
interval = 2*60 # time in minutes

# Pin numbers - change when connected
photodiode_filtered = 3
uv = 4
pir = 5

# NB: No need for photodiode to be connected 

GPIO.setmode(GPIO.BCM) # Not sure
GPIO.setwarnings(False) # Not sure

# Sets pins as digital in pins
GPIO.setup(photodiode_filtered,GPIO.IN) 
GPIO.setup(uv,GPIO.IN)
GPIO.setup(pir,GPIO.IN) 

def light(): # In the format (artificial, natural)
    return (GPIO.input(photodiode_filtered) == 1, GPIO.input(uv) == 1)

def motion():
    return GPIO.input(pir) == 1

def analysis(artificial_light, motion):
    return artificial_light and not motion


while True:
    light = light()
    artificial_light = light[0]
    natural_light = light[1]
    motion = motion()
    
    wasted_mins += int(analysis(artificial_light, motion)) * interval
    
    time.sleep(interval)