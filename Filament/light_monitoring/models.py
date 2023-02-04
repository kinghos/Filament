from django.db import models

class Data_Entry(models.Model):
    startTime = models.DateTimeField(default=None)
    endTime = models.DateTimeField(default=None)
    
    def __str__(self):
        start = self.startTime.strftime("%H:%M:%S %d-%m-%Y")
        end = self.endTime.strftime("%H:%M:%S %d-%m-%Y")
        return f"{start} — {end}"

    class Meta:
        app_label  = 'light_monitoring' # Needed for dataSaving.py

class Region(models.Model):
    region = models.CharField(max_length=2)
