from rest_framework import serializers

from .models import GPSPosicion, EventoDesvio


class EventoDesvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoDesvio
        fields = "__all__"


class GPSPosicionSerializer(serializers.ModelSerializer):
    # incluir eventos asociados (lista) de forma opcional
    eventos = EventoDesvioSerializer(many=True, read_only=True)

    class Meta:
        model = GPSPosicion
        fields = [
            "id",
            "ruta",
            "usuario",
            "longitud",
            "latitud",
            "velocidad",
            "fecha_hora",
            "eventos",
        ]
