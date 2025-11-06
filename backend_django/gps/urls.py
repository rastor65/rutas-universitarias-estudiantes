from django.urls import path
from .views import GPSCreateView, GPSNearbyView, GPSByRouteView, DeviceLatestView

urlpatterns = [
    path('', GPSCreateView.as_view(), name='gps-create'),                    # POST /api/gps/
    path('nearby/', GPSNearbyView.as_view(), name='gps-nearby'),             # GET /api/gps/nearby/?lat=&lng=&radius=
    path('route/<int:id_ruta>/', GPSByRouteView.as_view(), name='gps-route'),# GET /api/gps/route/1/
    path('device/<int:device_id>/latest/', DeviceLatestView.as_view(), name='device-latest'),
]
