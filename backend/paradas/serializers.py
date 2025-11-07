from rest_framework import serializers
from .models import Parada
from rutas.models import Ruta


class ParadaSerializer(serializers.ModelSerializer):
    """Serializador completo para el modelo Parada."""
    
    coordenadas = serializers.SerializerMethodField()
    ruta_nombre = serializers.CharField(source="ruta.nombre_ruta", read_only=True)
    
    class Meta:
        model = Parada
        fields = [
            "id",
            "nombre",
            "direccion",
            "coordenada_lat",
            "coordenada_lng",
            "coordenadas",
            "ruta",
            "ruta_nombre",
            "orden",
            "activa",
            "fecha_creacion",
            "fecha_actualizacion",
        ]
        read_only_fields = ["fecha_creacion", "fecha_actualizacion"]

    def get_coordenadas(self, obj):
        """Retorna las coordenadas en formato estándar."""
        return obj.coordenadas


class ParadaListSerializer(serializers.ModelSerializer):
    """Serializador simplificado para listados de paradas."""
    
    ruta_nombre = serializers.CharField(source="ruta.nombre_ruta", read_only=True)
    
    class Meta:
        model = Parada
        fields = [
            "id",
            "nombre",
            "direccion",
            "coordenada_lat",
            "coordenada_lng",
            "ruta",
            "ruta_nombre",
            "orden",
            "activa",
        ]


class ParadaCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializador para crear y actualizar paradas."""
    
    class Meta:
        model = Parada
        fields = [
            "nombre",
            "direccion",
            "coordenada_lat",
            "coordenada_lng",
            "ruta",
            "orden",
            "activa",
        ]

    def validate_ruta(self, value):
        """Valida que la ruta exista y esté activa."""
        if not value.capacidad_activa:
            raise serializers.ValidationError("La ruta no está activa.")
        return value

    def validate(self, data):
        """Validaciones adicionales."""
        # Validar que las coordenadas estén en rangos válidos
        lat = data.get("coordenada_lat")
        lng = data.get("coordenada_lng")
        
        if lat and (lat < -90 or lat > 90):
            raise serializers.ValidationError({
                "coordenada_lat": "La latitud debe estar entre -90 y 90 grados."
            })
        
        if lng and (lng < -180 or lng > 180):
            raise serializers.ValidationError({
                "coordenada_lng": "La longitud debe estar entre -180 y 180 grados."
            })
        
        return data
