import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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



def genWeekGraph(week, year):
    qs = Data_Entry.objects.filter(endTime__week = week).filter(endTime__year = year) # Generate a QuerySet of all of the data gathered during the given week in the given year
    durations = []
    datetimes = []
    for i in qs:
        durations.append(int((i.endTime - i.startTime).total_seconds()/60))
        datetimes.append(i.endTime)
    



    # Create a line plot
    plt.plot(datetimes, durations)
    myFmt = mdates.DateFormatter('%Y-%m-%d')
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.gcf().autofmt_xdate()

    # Add axis labels
    plt.xlabel('Date')
    plt.ylabel('Duration')

    # Show the plot
    plt.savefig(r'C:\Users\user\Documents\Homework\Young Engineers\FilamentProj\Filament\light_monitoring\graphs\graphs.png')
    plt.show()
    plt.close()

genWeekGraph(datetime.datetime.now().isocalendar()[1], datetime.datetime.now().year)