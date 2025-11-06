from rest_framework import serializers
from .models import Route, Device, GPSEvent, GPSPosition
from django.contrib.auth import get_user_model

User = get_user_model()

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'nombre', 'descripcion', 'activo', 'creado_en']

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'imei', 'nombre', 'activo', 'creado_en', 'ultima_posicion']

class GPSEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPSEvent
        fields = ['id', 'codigo', 'descripcion']

class GPSPositionSerializer(serializers.ModelSerializer):
    distancia_m = serializers.FloatField(read_only=True)

    class Meta:
        model = GPSPosition
        fields = [
            'id', 'id_ruta', 'id_usuario', 'device',
            'longitud', 'latitud', 'velocidad', 'heading', 'altitude',
            'accuracy', 'battery', 'fecha_hora', 'id_evento', 'distancia_m'
        ]
        read_only_fields = ['id', 'fecha_hora', 'distancia_m']

    def create(self, validated_data):
        # crear posición; el save() del modelo populá geom automáticamente
        return super().create(validated_data)
