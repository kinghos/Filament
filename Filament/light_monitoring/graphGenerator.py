#------------------------------------------Thorium - PA Pi---------------------------------------------
# Averages and graph code, V2
#  - Author & Date: Kingshuk, 28.1.22
#  - Description: Grabs data from the database
#    Contains functions for calculating daily, weekly, monthly and yearly averages
#    All functions return a tuple containing total time lights were on, and the average in that period
#    Uses said averages to generate graphs for each time period
#------------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import django
from django.conf import settings
from pathlib import Path
import matplotlib.font_manager as font_manager
from calendar import month_name

BASE_DIR = Path(__file__).resolve().parent.parent
if not settings.configured:
    settings.configure(DATABASES= {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }})
django.setup()

from .models import *

# AVERAGES
def secondsUnitConv(secondsTup):
    res = []
    for i in secondsTup:
        if i == 0:
            res.append("0 seconds")
        minutes, i = divmod(i, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        result = []

        if days > 0:
            result.append(f"{days:.0f} day{'s' if days > 1 else ''}")
        if hours > 0:
            result.append(f"{hours:.0f} hour{'s' if hours > 1 else ''}")
        if minutes > 0:
            result.append(f"{minutes:.0f} minute{'s' if minutes > 1 else ''}")
        if i > 0:
            result.append(f"{i:.0f} second{'s' if i > 1 else ''}")
        res.append(", ".join(result))

    res = list(filter(None, res))
    return res


def calcDayAverage(date):
    qs = Data_Entry.objects.filter(endTime__date = date) # Generate a QuerySet of all of the data gathered at the given date
    durations = []
    for i in qs:
        durations.append(int((i.endTime - i.startTime).total_seconds()))
    tot = sum(durations)
    try:
        avg = tot / len(durations)
        return tot, avg
    except ZeroDivisionError:
        return 0, 0


def calcWeekAverage(week, year):
    qs = Data_Entry.objects.filter(endTime__week = week).filter(endTime__year = year) # Generate a QuerySet of all of the data gathered during the given week in the given year
    durations = []
    for i in qs:
        durations.append(int((i.endTime - i.startTime).total_seconds()))
    tot = sum(durations)
    try:
        avg = tot / len(durations)
        return tot, avg
    except ZeroDivisionError:
        return 0, 0
    


def calcMonthAverage(month, year):
    qs = Data_Entry.objects.filter(endTime__month = month).filter(endTime__year = year) # Generate a QuerySet of all of the data gathered during the given month in the given year
    durations = []
    for i in qs:
        durations.append(int((i.endTime - i.startTime).total_seconds()))
    tot = sum(durations)
    try:
        avg = tot / len(durations)
        return tot, avg
    except ZeroDivisionError:
        return 0, 0


def calcYearAverage(year):
    qs = Data_Entry.objects.filter(endTime__year = year) # Generate a QuerySet of all of the data gathered during the given year
    durations = []
    for i in qs:
        durations.append(int((i.endTime - i.startTime).total_seconds()))
    tot = sum(durations)
    try:
        avg = tot / len(durations)
        return tot, avg
    except ZeroDivisionError:
        return 0, 0
    
# GRAPHS
def findWeekDates(week, year):
    d = datetime.strptime(f"{year}-W{week}-1", "%Y-W%U-%w")
    return [d + timedelta(days=i) for i in range(7)]

def getDatesInMonth(month, year):
    # Get the first and last day of the month
    firstDay = datetime(year, month, 1)
    if month == 12:
        lastDay = datetime(year+1, 1, 1) - timedelta(days=1)
    else:
        lastDay = datetime(year, month+1, 1) - timedelta(days=1)

    # Create a list of every date in the month
    dates = []
    currentDay = firstDay
    while currentDay <= lastDay:
        dates.append(currentDay)
        currentDay += timedelta(days=1)
    return dates

# Color constants
BGCOL = "#0f0f0f"
PLOTCOL = "#3b3b3b"
LINECOL = "#aaaaaa"
LABELCOL = "#aaaaaa"
BORDCOL = "#aaaaaa"

def formatGraph(dateFormat, figNo):
    plt.figure(figNo)
    plt.switch_backend('agg')


    
    # Get font
    font_dir = ['\static\light_monitoring\OpenSans-Regular.ttf']
    for font in font_manager.findSystemFonts(font_dir):
        font_manager.fontManager.addfont(font)

    plt.rcParams["font.family"] = "Open Sans"
    
    

    # Format the line plot
    myFmt = mdates.DateFormatter(dateFormat)
    plt.gcf().autofmt_xdate()
    plt.gcf().set_size_inches(10, 7)
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.gcf().set_facecolor(BGCOL)
    
    plt.gca().spines['left'].set_color(BORDCOL)        
    plt.gca().spines['top'].set_color(BORDCOL)         
    plt.gca().spines['bottom'].set_color(BORDCOL)         
    plt.gca().spines['right'].set_color(BORDCOL)         
    plt.gca().set_facecolor(PLOTCOL)

    plt.tick_params(axis='x', labelcolor=LABELCOL)
    plt.tick_params(axis='y', labelcolor=LABELCOL)


def genWeekGraph(week, year):
    figNo = 1
    plt.figure(figNo)

    weekDatesList = findWeekDates(week, year)
    durations = []
    for date in weekDatesList:
        durations.append(calcDayAverage(date.date()))
    durations = [i[1] for i in durations]

    # Add axis labels
    startDate = weekDatesList[0].strftime("%d-%m-%Y")
    endDate = weekDatesList[-1].strftime("%d-%m-%Y")
    plt.gca().set_title(f"Daily averages of energy waste from light, {startDate} - {endDate}", color=LABELCOL)
    plt.gca().set_xlabel('Date', color=LABELCOL)
    plt.gca().set_ylabel('Duration', color=LABELCOL)

    # Show the plot
    formatGraph('%d-%m-%Y', figNo)
    plt.plot(weekDatesList, durations, color=LINECOL)
    plt.savefig(r'C:\Users\user\Documents\Homework\Young Engineers\FilamentProj\Filament\light_monitoring\static\graphs\weekAvgGraph.png')

def genMonthGraph(month, year):
    figNo = 2
    plt.figure(figNo)

    durations = []
    dates = getDatesInMonth(month, year)
    for date in dates:
        durations.append(calcDayAverage(date.date()))
    durations = [i[1] for i in durations]

    # Add axis labels
    monthName = month_name[month]
    plt.gca().set_title(f"Daily averages of energy waste from light, {monthName}", color=LABELCOL)
    plt.gca().set_xlabel('Date', color=LABELCOL)
    plt.gca().set_ylabel('Duration', color=LABELCOL)

    # Show the plot
    formatGraph('%d-%m-%Y', figNo)
    plt.plot(dates, durations, color=LINECOL)
    ticks = plt.gca().xaxis.get_major_ticks()
    ticks[-1].label1.set_visible(False) # Hides last value (graph goes outside of month)

    plt.savefig(r'C:\Users\user\Documents\Homework\Young Engineers\FilamentProj\Filament\light_monitoring\static\graphs\monthAvgGraph.png')

week = (datetime.now() - timedelta(weeks=1)).isocalendar()[1]
year = datetime.now().year
month = (datetime.now()- timedelta(days=datetime.now().day)).month 
genWeekGraph(week, year)
genMonthGraph(month, year)

