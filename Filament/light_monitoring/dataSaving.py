import datetime
import django
from django.conf import settings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
settings.configure(DATABASES= {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }})
        
django.setup()

from models import *



def fetchData(): # Retrieves data from light sensing file; not implemented yet
    # Placeholder vars
    START_TIME = datetime.datetime.now() - datetime.timedelta(seconds=50)
    END_TIME = datetime.datetime.now()

    return START_TIME, END_TIME


start, end = fetchData()
newEntry = Data_Entry(startTime=start, endTime=end)
print(f"Duration = {newEntry}")
newEntry.save()
