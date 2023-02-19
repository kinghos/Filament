from django.shortcuts import render
from .models import *
from light_monitoring.graphGenerator import *
from .API import emissionsCalc, energyPrices
from .forms import SettingsForm
from django.views.generic import TemplateView

def filament(request):
    now = datetime.now()

    dayTot = secondsUnitConv(getTot(day=now.date())[0])
    weekTot = secondsUnitConv(getTot(week=now.isocalendar()[1], year=now.year)[0])
    monthTot = secondsUnitConv(getTot(month=now.month, year=now.year)[0])
    yearTot = secondsUnitConv(getTot(year=now.year)[0])


    dayAvg = secondsUnitConv(calcDayAverage(now))
    weekAvg = secondsUnitConv(calcWeekAverage(now.isocalendar()[1], now.year))
    monthAvg = secondsUnitConv(calcMonthAverage(now.month, now.year))
    yearAvg = secondsUnitConv(calcYearAverage(now.year))

    DNO = SettingsData.objects.last().region if SettingsData.objects.last().region else "10"
    energyCosts = energyPrices.getEnergyCosts(DNO)
    power  = SettingsData.objects.last().bulbPower
    time = 1 
    numBulbs = SettingsData.objects.last().numBulbs
    
    
    context = {
        "dailyAvg": dayAvg,
        "dayTot": dayTot,
        "weeklyAvg": weekAvg,
        "weekTot": weekTot,
        "monthlyAvg": monthAvg,
        "month": monthTot,
        "yearlyAvg": yearAvg,
        "yearTot": yearTot,
        "dailyCosts": f"{energyPrices.calcPrices(power, getTot(day=now.date())[0] / 3600, numBulbs, energyCosts):.2f}",
        "weeklyCosts": f"{energyPrices.calcPrices(power, getTot(week=now.isocalendar()[1], year=now.year)[0] / 3600, numBulbs, energyCosts):.2f}",

    }
    return render(request, 'light_monitoring/filament.html', context)

def data(request):
    context = {
        "data_entries": Data_Entry.objects.all().order_by("endTime")
    }
    return render(request, 'light_monitoring/data.html', context)

class SettingsView(TemplateView):
    template_name = "light_monitoring/settings.html"

    def get(self, request):
        form = SettingsForm()
        region = SettingsData.objects.first().region
        context = {
            "form": form,
            "region": region,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = SettingsForm(request.POST)

        if form.is_valid():
            form.save()
            region = form.cleaned_data["region"]
            numBulbs = form.cleaned_data["numBulbs"]
            bulbPower = form.cleaned_data["bulbPower"]
            bulbType = form.cleaned_data["bulbType"]
        else:
            form = SettingsForm()

        context = {
            "form": form,
            "region": region,
            "numBulbs": numBulbs,
            "bulbPower": bulbPower,
            "bulbType": bulbType,
        }
        return render(request, self.template_name, context)
