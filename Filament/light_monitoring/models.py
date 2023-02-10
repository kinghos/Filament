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

class SettingsData(models.Model):
    region = models.CharField(max_length=2)
    numBulbs = models.IntegerField(default=1)
    bulbPower = models.IntegerField(default=50, blank=True)
    bulbType = models.CharField(max_length=20, default="N/A", blank=True)
    @classmethod
    def object(cls):
        return cls._default_manager.all().first() # Since only one item

    def save(self, *args, **kwargs):
        self.pk = self.id = 1
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.region}, {self.numBulbs}, {self.bulbPower}, {self.bulbType}"

    class Meta:
        app_label = 'light_monitoring' # Needed for dataSaving.py

