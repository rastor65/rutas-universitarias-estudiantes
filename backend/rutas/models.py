from django.db import models


class Ruta(models.Model):
    nombre_ruta = models.CharField(max_length=100, verbose_name="Nombre de la ruta")
    capacidad_activa = models.IntegerField(blank=True, null=True, verbose_name="Capacidad activa")
    capacidad_espera = models.IntegerField(blank=True, null=True, verbose_name="Capacidad de espera")

    # Relación muchos a muchos con Bus
    buses = models.ManyToManyField(
        'Bus',
        related_name='rutas',
        blank=True,
        verbose_name='Buses asignados'
    )

    def __str__(self):
        return self.nombre_ruta

    class Meta:
        verbose_name = "Ruta"
        verbose_name_plural = "Rutas"


class Bus(models.Model):
    placa = models.CharField(max_length=10, unique=True, verbose_name="Placa del bus")
    marca = models.CharField(max_length=50, verbose_name="Marca del bus")
    modelo = models.CharField(max_length=50, verbose_name="Modelo del bus")
    capacidad = models.IntegerField(blank=True, null=True, verbose_name="Capacidad del bus")
    estado_bus = models.CharField(max_length=50, verbose_name="Estado del bus")

    def __str__(self):
        return f"{self.placa} - {self.marca}"

    class Meta:
        verbose_name = "Bus"
        verbose_name_plural = "Buses"


class TipoEstado(models.Model):
    nombre_estado = models.CharField(max_length=100, verbose_name="Nombre del estado")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción del estado")

    # Muchos estados pertenecen a una ruta
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE, related_name="tipos_estado")

    def __str__(self):
        return self.nombre_estado

    class Meta:
        verbose_name = "Tipo de Estado"
        verbose_name_plural = "Tipos de Estado"
