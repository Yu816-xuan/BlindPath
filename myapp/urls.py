from django.urls import path
from .views import home, monitoring_statistics, map_view
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('monitoring_statistics/', monitoring_statistics, name='monitoring_statistics'),
    path('map/', views.map_view, name='map_view'),
    path('api/monitor/<int:monitor_id>/details/', views.monitor_details, name='monitor_details'),
    path('api/monitor/<int:monitor_id>/alarms/', views.get_alarms_for_monitor, name='get_alarms_for_monitor'),
    path('api/monitor/<int:monitor_id>/alarms/update/', views.update_alarm_status, name='update_alarm_status'),
]
