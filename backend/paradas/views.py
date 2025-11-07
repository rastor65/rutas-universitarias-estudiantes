from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Parada
from .serializers import (
    ParadaSerializer,
    ParadaListSerializer,
    ParadaCreateUpdateSerializer
)


class ParadaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar paradas de bus.
    
    Endpoints:
    - GET /api/paradas/ - Lista todas las paradas
    - POST /api/paradas/ - Crea una nueva parada
    - GET /api/paradas/{id}/ - Obtiene detalles de una parada
    - PUT /api/paradas/{id}/ - Actualiza una parada
    - PATCH /api/paradas/{id}/ - Actualiza parcialmente una parada
    - DELETE /api/paradas/{id}/ - Elimina una parada
    - GET /api/paradas/por-ruta/?ruta_id={id} - Lista paradas por ruta
    - GET /api/paradas/activas/ - Lista solo paradas activas
    - GET /api/paradas/cercanas/?lat={lat}&lng={lng}&radio={km} - Busca paradas cercanas
    """
    
    queryset = Parada.objects.all().select_related("ruta")
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["ruta", "activa", "orden"]
    search_fields = ["nombre", "direccion"]
    ordering_fields = ["orden", "nombre", "fecha_creacion"]
    ordering = ["orden"]

    def get_serializer_class(self):
        """Retorna el serializador apropiado según la acción."""
        if self.action == "list":
            return ParadaListSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return ParadaCreateUpdateSerializer
        return ParadaSerializer

    @action(detail=False, methods=["get"], url_path="por-ruta")
    def por_ruta(self, request):
        """Lista las paradas de una ruta específica ordenadas por secuencia."""
        ruta_id = request.query_params.get("ruta_id")
        
        if not ruta_id:
            return Response(
                {"error": "El parámetro 'ruta_id' es requerido."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        paradas = self.queryset.filter(ruta_id=ruta_id, activa=True).order_by("orden")
        serializer = ParadaListSerializer(paradas, many=True)
        
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def activas(self, request):
        """Lista todas las paradas activas."""
        paradas = self.queryset.filter(activa=True)
        serializer = ParadaListSerializer(paradas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def cercanas(self, request):
        """
        Busca paradas cercanas a una ubicación dada.
        Parámetros: lat, lng, radio (en kilómetros, default=5)
        """
        lat = request.query_params.get("lat")
        lng = request.query_params.get("lng")
        radio = float(request.query_params.get("radio", 5))
        
        if not lat or not lng:
            return Response(
                {"error": "Los parámetros 'lat' y 'lng' son requeridos."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            lat = float(lat)
            lng = float(lng)
        except ValueError:
            return Response(
                {"error": "Las coordenadas deben ser números válidos."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cálculo aproximado de rango en grados (1 grado ≈ 111 km)
        delta = radio / 111.0
        
        paradas = self.queryset.filter(
            coordenada_lat__range=(lat - delta, lat + delta),
            coordenada_lng__range=(lng - delta, lng + delta),
            activa=True
        )
        
        serializer = ParadaListSerializer(paradas, many=True)
        return Response({
            "radio_km": radio,
            "centro": {"lat": lat, "lng": lng},
            "paradas": serializer.data
        })

    @action(detail=True, methods=["patch"])
    def toggle_activa(self, request, pk=None):
        """Activa o desactiva una parada."""
        parada = self.get_object()
        parada.activa = not parada.activa
        parada.save()
        
        serializer = self.get_serializer(parada)
        return Response(serializer.data)
