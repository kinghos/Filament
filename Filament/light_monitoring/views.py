from django.shortcuts import render
from .models import Data_Entry
from light_monitoring.graphGenerator import *
from .API import emissionsCalc, energyPrices
    
def filament(request):
    now = datetime.now()
    dayTot, dayAvg = secondsUnitConv(calcDayAverage(now))
    weekTot, weekAvg = secondsUnitConv(calcWeekAverage(now.isocalendar()[1], now.year))
    monthTot, monthAvg = secondsUnitConv(calcMonthAverage(now.month, now.year))
    yearTot, yearAvg = secondsUnitConv(calcYearAverage(now.year))

    energyCosts = energyPrices.getEnergyCosts()
    power = 50
    time = 1
    numBulbs = 1
    
    print(type(energyCosts))
    context = {
        "dailyAvg": dayAvg,
        "dayTot": dayTot,
        "weeklyAvg": weekAvg,
        "weekTot": weekTot,
        "monthlyAvg": monthAvg,
        "month": monthTot,
        "yearlyAvg": yearAvg,
        "yearTot": yearTot,
        "dailyCosts": f"{energyPrices.calcPrices(power, time, numBulbs, energyCosts):.2f}",
        "weeklyCosts": f"{energyPrices.calcPrices(power, time, numBulbs, energyCosts):.2f}",

    }
    return render(request, 'light_monitoring/filament.html', context)

def data(request):
    context = {
        "data_entries": Data_Entry.objects.all().order_by("endTime")
    }
    return render(request, 'light_monitoring/data.html', context)

def settings(request):
    return render(request, 'light_monitoring/settings.html')

