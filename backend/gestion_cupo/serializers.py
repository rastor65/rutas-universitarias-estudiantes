from rest_framework import serializers
from .models import Reserva, ListaDeEspera
from accounts.models import User


class UserSimpleSerializer(serializers.ModelSerializer):
    """Serializer simplificado para mostrar datos básicos del usuario"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class ReservaSerializer(serializers.ModelSerializer):
    usuario = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Reserva
        fields = [
            'id',
            'usuario',
            'ruta',
            'fecha_reserva',
            'updated_at',
            'estado',
            'motivo_cancelacion',
        ]
        read_only_fields = ['id', 'fecha_reserva', 'updated_at']

    def create(self, validated_data):
        # El usuario se asigna automáticamente desde la vista
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['usuario'] = request.user
        return super().create(validated_data)


class ListaDeEsperaSerializer(serializers.ModelSerializer):
    usuario = UserSimpleSerializer(read_only=True)

    class Meta:
        model = ListaDeEspera
        fields = [
            'id',
            'usuario',
            'ruta',
            'posicion',
            'fecha_inscripcion',
            'updated_at',
            'estado',
        ]
        read_only_fields = ['id', 'fecha_inscripcion', 'updated_at']

    def create(self, validated_data):
        # Igual que en reserva, el usuario se asigna automáticamente
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['usuario'] = request.user
        return super().create(validated_data)
