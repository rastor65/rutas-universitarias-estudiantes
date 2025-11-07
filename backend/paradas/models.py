from django.db import models
from rutas.models import Ruta
# from gps.models import GPSPosicion


class Parada(models.Model):
    """Representa una parada de bus en una ruta específica.
    
    Campos principales:
    - nombre: nombre de la parada
    - direccion: dirección física de la parada
    - coordenada_lat: latitud de la parada
    - coordenada_lng: longitud de la parada
    - ruta: FK a rutas.Ruta
    """
    
    nombre = models.CharField(max_length=200, verbose_name="Nombre de la parada")
    direccion = models.CharField(max_length=300, verbose_name="Dirección")
    coordenada_lat = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        verbose_name="Latitud"
    )
    coordenada_lng = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        verbose_name="Longitud"
    )
    ruta = models.ForeignKey(
        Ruta,
        on_delete=models.CASCADE,
        related_name="paradas_gestionadas",
        verbose_name="Ruta"
    )
    # Se puede agregar después con una migración cuando GPS esté implementado
    # posicion_gps = models.ForeignKey(
    #     'gps.GPSPosicion',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name="paradas_asociadas",
    #     verbose_name="Posición GPS"
    # )
    orden = models.IntegerField(
        default=0,
        verbose_name="Orden en la ruta",
        help_text="Orden de la parada en la secuencia de la ruta"
    )
    activa = models.BooleanField(
        default=True,
        verbose_name="Parada activa"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Parada"
        verbose_name_plural = "Paradas"
        ordering = ["ruta", "orden", "nombre"]
        indexes = [
            models.Index(fields=["ruta", "orden"]),
            models.Index(fields=["coordenada_lat", "coordenada_lng"]),
        ]

    def __str__(self):
        return f"{self.nombre} - {self.ruta.nombre_ruta if self.ruta else 'Sin ruta'}"

    @property
    def coordenadas(self):
        """Retorna las coordenadas como un diccionario."""
        return {
            "lat": float(self.coordenada_lat),
            "lng": float(self.coordenada_lng)
        }
