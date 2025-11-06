from django.urls import path
from .views import (
    ReservaListCreateView,
    ReservaDetailView,
    ListaDeEsperaListCreateView,
    ListaDeEsperaDetailView,
)

urlpatterns = [
    # Rutas de reservas
    path('reservas/', ReservaListCreateView.as_view(), name='reserva-list-create'),
    path('reservas/<uuid:pk>/', ReservaDetailView.as_view(), name='reserva-detail'),

    # Rutas de lista de espera
    path('lista-espera/', ListaDeEsperaListCreateView.as_view(), name='lista-espera-list-create'),
    path('lista-espera/<uuid:pk>/', ListaDeEsperaDetailView.as_view(), name='lista-espera-detail'),
]
