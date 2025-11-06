from rest_framework import serializers
from .models import ReservaCupo


class ReservaCupoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo ReservaCupo con validación automática
    de capacidad. Si se supera la capacidad del bus o ruta, el estado
    pasa a 'EN_ESPERA'.
    """

    class Meta:
        model = ReservaCupo
        fields = '__all__'

    def create(self, validated_data):
        ruta = validated_data.get('ruta')
        estado = validated_data.get('estado', 'ACTIVA')

        # Contar cuántas reservas activas existen actualmente
        reservas_activas = ReservaCupo.objects.filter(ruta=ruta, estado='ACTIVA').count()

        if ruta and ruta.capacidad_activa and reservas_activas >= ruta.capacidad_activa:
            # Si la capacidad se supera, poner en lista de espera
            validated_data['estado'] = 'EN_ESPERA'
        else:
            validated_data['estado'] = estado

        return super().create(validated_data)
