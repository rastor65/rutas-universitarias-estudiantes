from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import GPSPosition, Device, Route
from .serializers import GPSPositionSerializer
from django.db import transaction

class GPSCreateView(APIView):
    def post(self, request):
        data = request.data.copy()
        serializer = GPSPositionSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                obj = serializer.save()
            return Response(GPSPositionSerializer(obj).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GPSNearbyView(APIView):
    def get(self, request):
        try:
            lat = float(request.query_params.get('lat'))
            lng = float(request.query_params.get('lng'))
        except (TypeError, ValueError):
            return Response({'error': 'Parámetros lat y lng requeridos (float).'}, status=status.HTTP_400_BAD_REQUEST)
        radius = float(request.query_params.get('radius', 500))
        since = request.query_params.get('since')
        until = request.query_params.get('until')
        
        # Usar el manager personalizado para buscar puntos cercanos
        nearby_positions = GPSPosition.objects.within_radius(lng, lat, meters=radius, since=since, until=until)
        serializer = GPSPositionSerializer(nearby_positions, many=True)
        return Response(serializer.data)

class GPSByRouteView(APIView):
    def get(self, request, id_ruta):
        route = get_object_or_404(Route, pk=id_ruta)
        since = request.query_params.get('since')
        until = request.query_params.get('until')
        qs = GPSPosition.objects.filter(id_ruta=route)
        if since:
            qs = qs.filter(fecha_hora__gte=since)
        if until:
            qs = qs.filter(fecha_hora__lte=until)
        qs = qs.order_by('fecha_hora')
        serializer = GPSPositionSerializer(qs, many=True)
        return Response(serializer.data)

class DeviceLatestView(APIView):
    def get(self, request, device_id):
        device = get_object_or_404(Device, pk=device_id)
        pos = GPSPosition.objects.filter(device=device).order_by('-fecha_hora').first()
        if not pos:
            return Response({'detail': 'Sin posiciones para este dispositivo.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = GPSPositionSerializer(pos)
        return Response(serializer.data)
