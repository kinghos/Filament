#------------------------------------------Thorium - PA Pi---------------------------------------------
# Energy price calculation code
#  - Author & Date: Kingshuk, 22.1.22
#  - Description: Grabs data from the database
#    Contains functions for calculating daily, weekly, monthly and yearly averages
#    All functions return a tuple containing total time lights were on, and the average in that period
#------------------------------------------------------------------------------------------------------

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


def secondsUnitConv(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    result = []

    if days > 0:
        result.append(f"{days} day{'s' if days > 1 else ''}")
    if hours > 0:
        result.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0:
        result.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    if seconds > 0:
        result.append(f"{seconds} second{'s' if seconds > 1 else ''}")
    return ", ".join(result)


def calcDayAverage(date):
    qs = Data_Entry.objects.filter(endTime__date = date) # Generate a QuerySet of all of the data gathered at the given date
    durations = []
    for i in qs:
        durations.append(int((i.endTime - i.startTime).total_seconds()))
    tot = sum(durations)
    avg = tot / len(durations)
    return secondsUnitConv(tot), secondsUnitConv(avg)


def calcWeekAverage(week, year):
    qs = Data_Entry.objects.filter(endTime__week = week).filter(endTime__year = year) # Generate a QuerySet of all of the data gathered during the given week in the given year
    durations = []
    for i in qs:
        durations.append(int((i.endTime - i.startTime).total_seconds()))
    tot = sum(durations)
    avg = tot / len(durations)
    return secondsUnitConv(tot), secondsUnitConv(avg)


def calcMonthAverage(month, year):
    qs = Data_Entry.objects.filter(endTime__month = month).filter(endTime__year = year) # Generate a QuerySet of all of the data gathered during the given month in the given year
    durations = []
    for i in qs:
        durations.append(int((i.endTime - i.startTime).total_seconds()))
    tot = sum(durations)
    avg = tot / len(durations)
    return secondsUnitConv(tot), secondsUnitConv(avg)


def calcYearAverage(year):
    qs = Data_Entry.objects.filter(endTime__year = year) # Generate a QuerySet of all of the data gathered during the given year
    durations = []
    for i in qs:
        durations.append(int((i.endTime - i.startTime).total_seconds()))
    tot = sum(durations)
    avg = tot / len(durations)
    return secondsUnitConv(tot), secondsUnitConv(avg)


now = datetime.datetime.now()
weekNumber = now.isocalendar()[1]

day = calcDayAverage(now)
week = calcWeekAverage(weekNumber, now.year)
month = calcMonthAverage(now.month, now.year)
year = calcYearAverage(now.year)

print(f"Daily average: {day}\nWeekly average: {week}\nMonthly average: {month}\nYearly average: {year}")