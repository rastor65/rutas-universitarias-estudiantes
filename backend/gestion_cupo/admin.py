from django.contrib import admin
from .models import ReservaCupo


@admin.register(ReservaCupo)
class ReservaCupoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'ruta', 'estado', 'fecha_reserva', 'posicion_espera')
    list_filter = ('estado', 'ruta')
    search_fields = ('usuario__username', 'ruta__nombre_ruta')
    ordering = ('-fecha_reserva',)
