from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Ruta, Bus, TipoEstado
from .serializer import RutaSerializer, BusSerializer, TipoEstadoSerializer


class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer
    permission_classes = [AllowAny]


class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [AllowAny]


class TipoEstadoViewSet(viewsets.ModelViewSet):
    queryset = TipoEstado.objects.all()
    serializer_class = TipoEstadoSerializer
    permission_classes = [AllowAny]

