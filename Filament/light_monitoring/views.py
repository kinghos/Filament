from django.shortcuts import render
from .models import Data_Entry
from light_monitoring.graphGenerator import *
from .API import emissionsCalc, energyPrices
    
def filament(request):
    now = datetime.now()

    dayTup = secondsUnitConv(calcDayAverage(now))
    weekTup = secondsUnitConv(calcWeekAverage(now.isocalendar()[1], now.year))
    monthTup = secondsUnitConv(calcMonthAverage(now.month, now.year))
    yearTup = secondsUnitConv(calcYearAverage(now.year))


    dayTot, dayAvg = dayTup[0], dayTup[1]
    weekTot, weekAvg = weekTup[0], weekTup[1]
    monthTot, monthAvg = monthTup[0], monthTup[1]
    yearTot, yearAvg = yearTup[0], yearTup[1]

    energyCosts = energyPrices.getEnergyCosts()
    power = 50
    time = 1
    numBulbs = 1
    
    
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

