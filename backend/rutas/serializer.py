from rest_framework import serializers
from .models import Ruta, Bus, TipoEstado


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'


class RutaSerializer(serializers.ModelSerializer):
    # Mostramos los buses asociados
    buses = BusSerializer(many=True, read_only=True)

    class Meta:
        model = Ruta
        fields = '__all__'


class TipoEstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEstado
        fields = '__all__'

