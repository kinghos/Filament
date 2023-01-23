from django.shortcuts import render
from .models import Data_Entry
import datetime
from light_monitoring.averageCalc import *

def filament(request):
    now = datetime.datetime.now()
    dayTot, dayAvg = calcDayAverage(now)
    weekTot, weekAvg = calcWeekAverage(now.isocalendar()[1], now.year)
    monthTot, monthAvg = calcMonthAverage(now.month, now.year)
    yearTot, yearAvg = calcYearAverage(now.year)

    
    context = {
        "dailyAvg": dayAvg,
        "weeklyAvg": weekAvg,
        "monthlyAvg": monthAvg,
        "yearlyAvg": yearAvg,
    }
    return render(request, 'light_monitoring/filament.html', context)

def data(request):
    context = {
        "data_entries": Data_Entry.objects.all().order_by("endTime")
    }
    return render(request, 'light_monitoring/data.html', context)

def settings(request):
    return render(request, 'light_monitoring/settings.html')