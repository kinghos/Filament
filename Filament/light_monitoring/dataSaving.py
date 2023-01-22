#------------------------------------------Thorium - PA Pi-------------------------------------------
# Saving data to the Django database
#  - Author & Date: Kingshuk, 22.1.22
#  - Description: Grabs data from the light sensing file (uses placeholders currently, as light
#       sensing code is not yet complete)
#    Saves data to the database
#----------------------------------------------------------------------------------------------------

import datetime
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

from models import *



def fetchData(): # Retrieves data from light sensing file; not implemented yet
    # Placeholder vars
    START_TIME = datetime.datetime.now() - datetime.timedelta(seconds=60)
    END_TIME = datetime.datetime.now()

    return START_TIME, END_TIME


start, end = fetchData()
newEntry = Data_Entry(startTime=start, endTime=end)
newEntry.save()
