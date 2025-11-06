from django.urls import path
from .views import ReservaCupoListCreateView, ReservaCupoDetailView

urlpatterns = [
    # Listar todas las reservas o crear una nueva
    path('', ReservaCupoListCreateView.as_view(), name='reserva-list-create'),

    # Obtener, actualizar o eliminar una reserva específica por su UUID
    path('<uuid:pk>/', ReservaCupoDetailView.as_view(), name='reserva-detail'),
]
