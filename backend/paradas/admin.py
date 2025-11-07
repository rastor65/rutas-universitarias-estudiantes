from django.contrib import admin
from .models import Parada


@admin.register(Parada)
class ParadaAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "nombre",
        "ruta",
        "orden",
        "activa",
        "coordenada_lat",
        "coordenada_lng",
        "fecha_creacion",
    ]
    list_filter = ["activa", "ruta", "fecha_creacion"]
    search_fields = ["nombre", "direccion"]
    ordering = ["ruta", "orden", "nombre"]
    list_editable = ["activa", "orden"]
    readonly_fields = ["fecha_creacion", "fecha_actualizacion"]
    
    fieldsets = (
        ("Información básica", {
            "fields": ("nombre", "direccion", "activa")
        }),
        ("Ubicación", {
            "fields": ("coordenada_lat", "coordenada_lng")
        }),
        ("Ruta", {
            "fields": ("ruta", "orden")
        }),
        ("Fechas", {
            "fields": ("fecha_creacion", "fecha_actualizacion"),
            "classes": ("collapse",)
        }),
    )
