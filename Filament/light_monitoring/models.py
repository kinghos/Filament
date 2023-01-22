from django.db import models

class Data_Entry(models.Model):
    startTime = models.DateTimeField(default=None)
    endTime = models.DateTimeField(default=None)
    def __str__(self):
        duration = self.endTime - self.startTime
        return f"{duration.total_seconds()} seconds"
