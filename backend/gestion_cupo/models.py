import uuid
from django.db import models
from django.conf import settings


class Reserva(models.Model):
    ESTADOS = [
        ('RESERVADO', 'Reservado'),
        ('CANCELADO', 'Cancelado'),
        ('COMPLETADO', 'Completado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservas'
    )
    # Relación futura con la app de Rutas (pendiente de crear)
    ruta = models.UUIDField(blank=True, null=True, help_text="UUID de la ruta asignada")

    fecha_reserva = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    estado = models.CharField(max_length=15, choices=ESTADOS, default='RESERVADO')
    motivo_cancelacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reserva de {self.usuario.username} - Estado: {self.estado}"

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-fecha_reserva']
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'ruta'],
                name='unique_reserva_por_usuario_y_ruta'
            )
        ]


class ListaDeEspera(models.Model):
    ESTADOS = [
        ('EN_ESPERA', 'En Espera'),
        ('PASO_A_RESERVA', 'Pasó a Reserva'),
        ('CANCELADO', 'Cancelado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listas_espera'
    )
    ruta = models.UUIDField(blank=True, null=True, help_text="UUID de la ruta asociada")

    posicion = models.PositiveIntegerField(help_text="Posición actual en la lista de espera")
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='EN_ESPERA')

    def __str__(self):
        return f"Lista de espera #{self.posicion} - Usuario: {self.usuario.username}"

    class Meta:
        verbose_name = "Lista de Espera"
        verbose_name_plural = "Listas de Espera"
        ordering = ['posicion', 'fecha_inscripcion']
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'ruta'],
                name='unique_lista_espera_por_usuario_y_ruta'
            )
        ]
