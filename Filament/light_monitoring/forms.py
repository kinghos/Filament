from django import forms
from .models import Region

class SettingsForm(forms.ModelForm):
    REGION_CHOICES = (
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
    region = forms.ChoiceField(choices=REGION_CHOICES)

    class Meta:
        model = Region
        fields = {"region",}