from django.shortcuts import render
from .models import *
from light_monitoring.graphGenerator import *
from .API import emissionsCalc, energyPrices
from .forms import SettingsForm
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse

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
        "dataEntries": Data_Entry.objects.all().order_by("endTime")
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

def yearData(request, year):
    imgpath = fr"C:\Users\user\Documents\Homework\Young Engineers\FilamentProj\Filament\light_monitoring\static\graphs\queries\{year}"
    qs = Data_Entry.objects.filter(endTime__year=year)
    context = {
        'dataEntries': qs,
        "year":year
    }
    genYearGraph(year, imgpath)
    return render(request, 'light_monitoring/yearData.html', context)

def monthData(request, year, month):
    qs = Data_Entry.objects.filter(endTime__year=year, endTime__month=month)
    imgpath = fr"C:\Users\user\Documents\Homework\Young Engineers\FilamentProj\Filament\light_monitoring\static\graphs\queries\{year}_{month}"
    context = {
        'dataEntries': qs,
        "year": year,
        "month": month,
    }
    genMonthGraph(month, year, imgpath)
    return render(request, 'light_monitoring/monthData.html', context)

def dateData(request, year, month, day):
    qs = Data_Entry.objects.filter(endTime__year=year, endTime__month=month, endTime__day=day)
    imgpath = fr"C:\Users\user\Documents\Homework\Young Engineers\FilamentProj\Filament\light_monitoring\static\graphs\queries\{year}_{month}_{day}"
    context = {
        'dataEntries': qs,
        "year": year,
        "month": month,
        "day": day,
    }
    genDayGraph(datetime(year, month, day), imgpath)
    return render(request, 'light_monitoring/dateData.html', context)

def dataRedirect(request):
    date = request.GET.get('date')
    if date:
        c = date.count("/")
        if c == 0:
            return HttpResponseRedirect(reverse('yearData', args=[date]))
        elif c == 1:
            year, month = date.split('/')
            return HttpResponseRedirect(reverse('monthData', args=[year, month]))
        else:
            year, month, day = date.split("/")
            return HttpResponseRedirect(reverse('dateData', args=[year, month, day]))
    else:
        # Handle invalid form data
        pass

def advice(request):
    return render(request, "light_monitoring/advice.html")