from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import GPSPosicion, EventoDesvio
from .serializers import GPSPosicionSerializer, EventoDesvioSerializer


class GPSPosicionViewSet(viewsets.ModelViewSet):
	queryset = GPSPosicion.objects.all()
	serializer_class = GPSPosicionSerializer
	permission_classes = [AllowAny]


class EventoDesvioViewSet(viewsets.ModelViewSet):
	queryset = EventoDesvio.objects.all()
	serializer_class = EventoDesvioSerializer
	permission_classes = [AllowAny]

