from rest_framework import generics
from .models import ReservaCupo
from .serializers import ReservaCupoSerializer
from rest_framework.response import Response
from rest_framework import status

class ReservaCupoListCreateView(generics.ListCreateAPIView):
    queryset = ReservaCupo.objects.all()
    serializer_class = ReservaCupoSerializer

    def perform_create(self, serializer):
        # Lógica: si el bus está lleno, asignar estado "EN_ESPERA"
        bus = serializer.validated_data.get('bus')
        reservas_activas = ReservaCupo.objects.filter(bus=bus, estado='RESERVADO').count()
        capacidad = bus.capacidad  # Asegúrate que el modelo Bus tenga el campo "capacidad"

        if reservas_activas >= capacidad:
            serializer.save(estado='EN_ESPERA')
        else:
            serializer.save(estado='RESERVADO')


class ReservaCupoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReservaCupo.objects.all()
    serializer_class = ReservaCupoSerializer
