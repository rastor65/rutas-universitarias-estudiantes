from django.db import models

from rutas.models import Ruta


class GPSPosicion(models.Model):
	"""Representa una posición GPS registrada por un usuario o un bus.

	Campos principales:
	- ruta: FK a `rutas.Ruta` (opcional)
	- usuario: FK a `accounts.User` (opcional)
	- longitud/latitud: coordenadas decimales
	- velocidad: velocidad en km/h (opcional)
	- fecha_hora: marca temporal del dato GPS
	"""

	ruta = models.ForeignKey(Ruta, on_delete=models.SET_NULL, null=True, blank=True, related_name="posiciones")
	usuario = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="posiciones")
	longitud = models.DecimalField(max_digits=9, decimal_places=6)
	latitud = models.DecimalField(max_digits=9, decimal_places=6)
	velocidad = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
	fecha_hora = models.DateTimeField()

	class Meta:
		verbose_name = "GPS Posición"
		verbose_name_plural = "GPS Posiciones"
		ordering = ["-fecha_hora"]

	def __str__(self):
		u = self.usuario.username if self.usuario else "-"
		r = self.ruta.nombre_ruta if self.ruta else "-"
		return f"Posición {self.id} (usuario={u} ruta={r} @ {self.fecha_hora})"


class EventoDesvio(models.Model):
	"""Evento que indica un desvío u otro incidente asociado a una posición.

	Campos principales:
	- posicion: FK a `GPSPosicion` (opcional)
	- ruta: FK a `rutas.Ruta` (opcional)
	- fecha_hora: cuando ocurrió el evento
	- tipo_desvio: texto corto describiendo el tipo
	- estado: estado del evento (ej. abierto, cerrado)
	- descripcion: detalles adicionales
	"""

	posicion = models.ForeignKey(GPSPosicion, on_delete=models.SET_NULL, null=True, blank=True, related_name="eventos")
	ruta = models.ForeignKey(Ruta, on_delete=models.SET_NULL, null=True, blank=True, related_name="eventos")
	fecha_hora = models.DateTimeField()
	tipo_desvio = models.CharField(max_length=100)
	estado = models.CharField(max_length=50, default="abierto")
	descripcion = models.TextField(blank=True)

	class Meta:
		verbose_name = "Evento Desvío"
		verbose_name_plural = "Eventos Desvío"
		ordering = ["-fecha_hora"]

	def __str__(self):
		pos = f"pos={self.posicion.id}" if self.posicion else "pos=-"
		return f"Evento {self.id} ({self.tipo_desvio}) {pos} @ {self.fecha_hora}"

