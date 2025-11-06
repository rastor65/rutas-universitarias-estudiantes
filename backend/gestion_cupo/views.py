from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework import status

from .models import Reserva, ListaDeEspera
from .serializers import ReservaSerializer, ListaDeEsperaSerializer


# -------------------------------------
# RESERVAS
# -------------------------------------
class ReservaListCreateView(generics.ListCreateAPIView):
    """
    GET: lista todas las reservas del usuario autenticado.
    POST: crea una nueva reserva asociada al usuario actual.
    """
    serializer_class = ReservaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Solo muestra las reservas del usuario logueado
        return Reserva.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class ReservaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Permite ver, actualizar o eliminar una reserva específica.
    """
    serializer_class = ReservaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user)


# -------------------------------------
# LISTA DE ESPERA
# -------------------------------------
class ListaDeEsperaListCreateView(generics.ListCreateAPIView):
    """
    GET: lista todas las entradas en lista de espera del usuario autenticado.
    POST: crea una nueva entrada en lista de espera.
    """
    serializer_class = ListaDeEsperaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ListaDeEspera.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class ListaDeEsperaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Permite ver, actualizar o eliminar una entrada específica de la lista de espera.
    """
    serializer_class = ListaDeEsperaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ListaDeEspera.objects.filter(usuario=self.request.user)