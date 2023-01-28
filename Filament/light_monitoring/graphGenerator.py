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
            return "0 seconds"
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
    return res


def calcDayAverage(date, format=None):
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

def genWeekGraph(week, year):
    
    weekDatesList = findWeekDates(week, year)
    durations = []
    for date in weekDatesList:
        durations.append(calcDayAverage(date.date()))
    durations = [i[1] for i in durations]

    

    
    

    # Color constants
    BGCOL = "#0f0f0f"
    PLOTCOL = "#3b3b3b"
    LINECOL = "#aaaaaa"
    LABELCOL = "#aaaaaa"
    BORDCOL = "#aaaaaa"
    FONT = ""

    # Get font
    import matplotlib.font_manager as font_manager

    
    font_dir = ['\static\light_monitoring\OpenSans-Regular.ttf']
    for font in font_manager.findSystemFonts(font_dir):
        font_manager.fontManager.addfont(font)

    plt.rcParams["font.family"] = "Open Sans"
    
    

    # Format the line plot
    myFmt = mdates.DateFormatter('%d-%m-%Y')
    plt.gcf().autofmt_xdate()
    plt.gcf().set_size_inches(10, 7)
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.gcf().set_facecolor(BGCOL)
    

    # Add axis labels
    startDate = weekDatesList[0].strftime("%d-%m-%Y")
    endDate = weekDatesList[-1].strftime("%d-%m-%Y")
    plt.gca().set_title(f"Daily averages of energy waste from light, {startDate} - {endDate}", color=LABELCOL)
    plt.gca().set_xlabel('Date', color=LABELCOL)
    plt.gca().set_ylabel('Duration', color=LABELCOL)

    plt.gca().spines['left'].set_color(BORDCOL)        
    plt.gca().spines['top'].set_color(BORDCOL)         
    plt.gca().spines['bottom'].set_color(BORDCOL)         
    plt.gca().spines['right'].set_color(BORDCOL)         
    plt.gca().set_facecolor(PLOTCOL)

    plt.tick_params(axis='x', labelcolor=LABELCOL)
    plt.tick_params(axis='y', labelcolor=LABELCOL)

    # Show the plot
    plt.plot(weekDatesList, durations, color=LINECOL)
    plt.savefig(r'C:\Users\user\Documents\Homework\Young Engineers\FilamentProj\Filament\light_monitoring\static\graphs\weekAvgGraph.png')

week = datetime.now().isocalendar()[1] - 1
year = datetime.now().year
genWeekGraph(week, year)

