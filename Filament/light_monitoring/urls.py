from django.urls import path
from .views import *
from light_monitoring.views import SettingsView

urlpatterns = [
    path('', filament, name='filament'),
    path('data/', data, name="data"),
    path('data/redirect/', dataRedirect, name='dataRedirect'),
    path('data/<int:year>/', yearData, name='yearData'),
    path('data/<int:year>/<int:month>/', monthData, name='monthData'),
    path('data/<int:year>/<int:month>/<int:day>/', dateData, name='dateData'),
    path('settings/', SettingsView.as_view(), name="settings"),
]