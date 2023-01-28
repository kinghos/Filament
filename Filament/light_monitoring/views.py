from django.shortcuts import render
from .models import Data_Entry
from light_monitoring.graphGenerator import *
    
def filament(request):
    now = datetime.now()
    dayTot, dayAvg = secondsUnitConv(calcDayAverage(now))
    weekTot, weekAvg = secondsUnitConv(calcWeekAverage(now.isocalendar()[1], now.year))
    monthTot, monthAvg = secondsUnitConv(calcMonthAverage(now.month, now.year))
    yearTot, yearAvg = secondsUnitConv(calcYearAverage(now.year))

    
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

