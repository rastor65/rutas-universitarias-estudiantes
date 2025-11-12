import uuid
from django.db import models
from django.conf import settings
from rutas.models import Ruta


class ReservaCupo(models.Model):
    ESTADOS = [
        ('RESERVADO', 'Reservado'),
        ('EN_ESPERA', 'En Espera'),
        ('CANCELADO', 'Cancelado'),
        ('COMPLETADO', 'Completado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservas_cupo'
    )

    ruta = models.ForeignKey(
        Ruta,
        on_delete=models.CASCADE,
        related_name='reservas_cupo',
        help_text="Ruta asociada a la reserva"
    )

    fecha_reserva = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='RESERVADO')
    posicion_espera = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Posición en la lista de espera si aplica"
    )
    motivo_cancelacion = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return f"{self.usuario.username} - {self.ruta.nombre_ruta} ({self.estado})"

    class Meta:
        verbose_name = "Reserva de Cupo"
        verbose_name_plural = "Reservas de Cupos"
        ordering = ['-fecha_reserva']
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'ruta'],
                name='unique_reserva_cupo_por_usuario_y_ruta'
            )
        ]
