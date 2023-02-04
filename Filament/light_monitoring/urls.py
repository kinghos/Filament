from django.urls import path
from .views import *
from light_monitoring.views import SettingsView

urlpatterns = [
    path('', filament, name='filament'),
    path('data/', data, name="data"),
    path('settings/', SettingsView.as_view(), name="settings"),
]