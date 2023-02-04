from django.shortcuts import render
from .models import *
from light_monitoring.graphGenerator import *
from .API import emissionsCalc, energyPrices
from .forms import SettingsForm
from django.views.generic import TemplateView

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

    DNO = Region.objects.last().region if Region.objects.last().region != None else "10"
    print(DNO)
    energyCosts = energyPrices.getEnergyCosts(DNO)
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

class SettingsView(TemplateView):
    template_name = "light_monitoring/settings.html"

    def get(self, request):
        form = SettingsForm()
        region = Region.objects.first().region
        context = {
            "form": form,
            "region": region,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = SettingsForm(request.POST)

        if form.is_valid():
            Region.objects.all().delete()
            form.save()
            region = form.cleaned_data["region"]
        else:
            form = SettingsForm()

        context = {
            "form": form,
            "region": region,
        }
        return render(request, self.template_name, context)
