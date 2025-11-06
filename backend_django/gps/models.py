import math
from django.db import models
from django.conf import settings
from django.utils import timezone

# Modelo que representa una ruta/trayecto lógica
class Route(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.nombre}"


# Modelo que representa un dispositivo (por ejemplo, GPS/IMEI)
class Device(models.Model):
    imei = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150, blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    ultima_posicion = models.ForeignKey('GPSPosition', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    def __str__(self):
        return self.nombre or self.imei


# Modelo para tipificar eventos asociados a posiciones
class GPSEvent(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"


# Manager con helper para consultas espaciales comunes
class GPSPositionManager(models.Manager):
    def haversine_m(self, lon1, lat1, lon2, lat2):
        # retorna distancia en metros entre dos puntos (lon,lat)
        R = 6371000.0
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2.0)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def within_radius(self, lng, lat, meters=500, since=None, until=None, limit=1000):
        """
        Filtra posiciones dentro de un radio (metros) alrededor de (lng, lat)
        usando bounding box en DB y Haversine en Python para precisión.
        """
        # aprox. grados por metro
        delta_lat = meters / 111000.0
        lat_rad = math.radians(lat)
        delta_lng = meters / (111000.0 * max(math.cos(lat_rad), 0.000001))

        qs = self.get_queryset().filter(
            latitud__gte=lat - delta_lat,
            latitud__lte=lat + delta_lat,
            longitud__gte=lng - delta_lng,
            longitud__lte=lng + delta_lng
        )
        if since:
            qs = qs.filter(fecha_hora__gte=since)
        if until:
            qs = qs.filter(fecha_hora__lte=until)

        # materializar para calcular distancias en Python y ordenar por fecha_hora
        results = []
        for p in qs.order_by('fecha_hora'):
            d = self.haversine_m(lng, lat, p.longitud, p.latitud)
            if d <= meters:
                obj = p
                # adjuntar atributo temporal distancia_m
                setattr(obj, 'distancia_m', d)
                results.append(obj)
                if len(results) >= limit:
                    break
        return results


# Modelo principal de posiciones GPS
class GPSPosition(models.Model):
    # Mantengo nombres compatibles con tu esquema anterior (id_ruta, id_usuario)
    id_ruta = models.ForeignKey(Route, null=True, blank=True, on_delete=models.SET_NULL, db_column='id_ruta', related_name='posiciones')
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, db_column='id_usuario', related_name='posiciones')
    device = models.ForeignKey(Device, null=True, blank=True, on_delete=models.SET_NULL, related_name='posiciones')

    # Coordenadas redundantes para querys rápidas y compatibilidad
    longitud = models.FloatField()
    latitud = models.FloatField()

    # Datos de telemetría
    velocidad = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    heading = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    altitude = models.DecimalField(max_digits=9, decimal_places=3, null=True, blank=True)
    accuracy = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    battery = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    fecha_hora = models.DateTimeField(default=timezone.now)
    id_evento = models.ForeignKey(GPSEvent, null=True, blank=True, on_delete=models.SET_NULL)

    objects = GPSPositionManager()

    class Meta:
        ordering = ['-fecha_hora']
        indexes = [
            models.Index(fields=['fecha_hora'], name='gps_fecha_idx'),
            models.Index(fields=['latitud'], name='gps_lat_idx'),
            models.Index(fields=['longitud'], name='gps_lng_idx'),
        ]

    def save(self, *args, **kwargs):
        # asegurar coherencia (puedes agregar validaciones de rango)
        if self.longitud is None or self.latitud is None:
            raise ValueError("latitud y longitud son requeridos")
        super().save(*args, **kwargs)
        # actualizar ultima_posicion del dispositivo sin fallar
        try:
            if self.device_id:
                Device.objects.filter(pk=self.device_id).update(ultima_posicion=self)
        except Exception:
            pass

    def distancia_a(self, lng, lat):
        return GPSPosition.objects.haversine_m(self, lng, lat, self.longitud, self.latitud) if False else GPSPosition.objects.haversine_m(self, self.longitud, self.latitud, lng, lat)

    def __str__(self):
        return f"Posición {self.pk} ({self.latitud:.6f}, {self.longitud:.6f})"
