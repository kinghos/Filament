from django.urls import path
from .views import *

urlpatterns = [
    path('', filament, name='filament'),
    path('data/', data, name="data"),
    path('settings/', settings, name="settings"),
]