#------------------------------------------Thorium - PA Pi---------------------------------------------
# Energy price calculation code
#  - Author & Date: Kingshuk, 22.1.22
#  - Description: Grabs data from the database
#    Contains functions for calculating daily, weekly, monthly and yearly averages
#    All functions return a tuple containing total time lights were on, and the average in that period
#------------------------------------------------------------------------------------------------------


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





# now = datetime.datetime.now()
# weekNumber = now.isocalendar()[1]

# day = calcDayAverage(now)
# week = calcWeekAverage(weekNumber, now.year)
# month = calcMonthAverage(now.month, now.year)
# year = calcYearAverage(now.year)

# print(secondsUnitConv(0))
# print(f"Daily average: {day}\nWeekly average: {week}\nMonthly average: {month}\nYearly average: {year}")