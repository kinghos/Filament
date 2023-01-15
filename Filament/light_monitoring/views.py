from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Data_Entry
import datetime


def home(request):
    duration_tot = 0
    for i in Data_Entry.objects.all():
        duration = i.endTime - i.startTime
        duration_tot += duration.total_seconds()
    template = loader.get_template("light_monitoring/home.html")
    context = {
        'duration_tot': duration_tot,
    }
    return HttpResponse(template.render(context, request))