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

    @classmethod
    def object(cls):
        return cls._default_manager.all().first() # Since only one item

    def save(self, *args, **kwargs):
        self.pk = self.id = 1
        return super().save(*args, **kwargs)
    
    class Meta:
        app_label = 'light_monitoring' # Needed for dataSaving.py

