from django.db import models
from django.core.exceptions import ValidationError

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

    def save(self, *args, **kwargs):
        if not self.pk and Region.objects.exists():
            raise ValidationError('There can be only one Region instance')
        return super(Region, self).save(*args, **kwargs)
