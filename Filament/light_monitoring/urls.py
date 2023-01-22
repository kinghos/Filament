from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.data, name="data"),
    path('', views.settings, name="settings"),
]