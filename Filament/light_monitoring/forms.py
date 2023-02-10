from django import forms
from .models import SettingsData

class SettingsForm(forms.ModelForm):
    REGIONCHOICES = (
        (10, 'Eastern England'),
        (11, 'East Midlands'),
        (12, 'London'),
        (13, 'North Wales & Mersey'),
        (14, 'Midlands'),
        (15, 'North East'),
        (16, 'North West'),
        (17, 'Northern Scotland'),
        (18, 'Southern Scotland'),
        (19, 'South East'),
        (20, 'Southern'),
        (21, 'South Wales'),
        (22, 'South Western'),
        (23, 'Yorkshire')
    )
    BULBCHOICES = (
        ("N/A", "Unsure"),
        ("HAL", "Halogen"),
        ("FIL", "Filament"),
        ("LED", "LED"),
    )

    region = forms.ChoiceField(choices=REGIONCHOICES)
    numBulbs = forms.IntegerField()
    bulbPower = forms.IntegerField()
    bulbType = forms.ChoiceField(choices=BULBCHOICES)

    class Meta:
        model = SettingsData
        fields = ("region", "numBulbs", "bulbPower", "bulbType")