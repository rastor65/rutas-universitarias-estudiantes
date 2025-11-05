from django.contrib import admin
from .models import Reserva, ListaDeEspera


# === ADMIN PERSONALIZADOS ===
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "ruta", "estado", "fecha_reserva", "updated_at")
    list_filter = ("estado",)
    search_fields = ("usuario__username", "ruta")
    ordering = ("-fecha_reserva",)
    readonly_fields = ("fecha_reserva", "updated_at")


@admin.register(ListaDeEspera)
class ListaDeEsperaAdmin(admin.ModelAdmin):
    list_display = ("posicion", "usuario", "ruta", "estado", "fecha_inscripcion", "updated_at")
    list_filter = ("estado",)
    search_fields = ("usuario__username", "ruta")
    ordering = ("posicion", "fecha_inscripcion")
    readonly_fields = ("fecha_inscripcion", "updated_at")
