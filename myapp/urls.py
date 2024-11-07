# myapp/urls.py
from django.urls import path
from .views import home, monitoring_statistics, map_view
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('monitoring_statistics/', monitoring_statistics, name='monitoring_statistics'),
    path('map/', views.map_view, name='map_view'),
]
