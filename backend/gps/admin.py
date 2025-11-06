from django.contrib import admin

from .models import GPSPosicion, EventoDesvio


@admin.register(GPSPosicion)
class GPSPosicionAdmin(admin.ModelAdmin):
	list_display = ("id", "usuario", "ruta", "latitud", "longitud", "velocidad", "fecha_hora")
	list_filter = ("ruta", "fecha_hora")
	search_fields = ("usuario__username",)


@admin.register(EventoDesvio)
class EventoDesvioAdmin(admin.ModelAdmin):
	list_display = ("id", "tipo_desvio", "estado", "ruta", "posicion", "fecha_hora")
	list_filter = ("tipo_desvio", "estado", "ruta")
	search_fields = ("descripcion",)

