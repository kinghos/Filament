#------------------------------------------Thorium - PA Pi-------------------------------------------
# Sensor code V2 Testing purposes
#  - Author & Date: Umar and Kingshuk, 11.3.23
#  - Description: Finds time wasted from sensor data & when it is wasted
#                 Will only work at night as the photodiode serves only to tell if it is light or not
#                 The daylight API should say when to pause everything and to stop recording at day.
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

from models import Data_Entry


# GPIO Setup
GPIO.setmode(GPIO.BOARD)

# Pin numbers
photodiode = 3 # Using PIN 3 (GPIO 2) as Input
pir = 11 # Using PIN 5 (GPIO 3) as Input
 
# Sets pins as digital in pins
GPIO.setup(photodiode,GPIO.IN) 
GPIO.setup(pir,GPIO.IN)

# Globals & set-up
interval = 1 # Time in seconds
wasted_prev = False
motion_count = 0 # Refers to number of cycles where there is no motion
len_no_motion = 5 # How long does PIR need to output 0 for until it counts as 0


while True:
    light = GPIO.input(photodiode)
    motion = GPIO.input(11)
    print(f"light = {light} motion = {motion}")
    
    # For testing use without hardware connected - for a True input any string, for False press enter
    # light = bool(input('Light: '))
    # raw_motion = bool(input('Motion: '))
        
    wasted = False
    # no_motion = False
    
    # If there hasn't been motion for a while, then we can say there is no one in the room
    # if not raw_motion:
        # motion_count += 1
        # if motion_
        # count * interval > len_no_motion: # If the time the PIR has outputted 0 for is over X seconds:
            # no_motion = True
    # else:
        # motion_count = 0
    
    # If there is light and no-one in the room, set start to the time now
    if bool(light) and not bool(motion):
        wasted = True
        if not wasted_prev:
            start = datetime.datetime.now()
    
    # If X seconds ago, energy was being wasted, set end to time now
    elif wasted_prev:
        end = datetime.datetime.now()
        print(start, end)
        newEntry = Data_Entry(startTime=start, endTime=end)
        newEntry.save()
    
    wasted_prev = wasted
    
    print('Wasted:', wasted)
    # print('Start:', start, '\t', 'End:', end)
    print('\n')
    
    time.sleep(interval)
    
    
    