from django.contrib import admin
from .models import Ruta, Bus, TipoEstado


@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ("nombre_ruta", "capacidad_activa", "capacidad_espera", "mostrar_buses")
    search_fields = ("nombre_ruta",)
    list_filter = ("capacidad_activa", "capacidad_espera")
    ordering = ("nombre_ruta",)
    filter_horizontal = ("buses",)  # Esto sirve para editar el ManyToMany fácilmente en admin

    def mostrar_buses(self, obj):
        # Muestra todas las placas de los buses asociados
        return ", ".join([bus.placa for bus in obj.buses.all()])

    mostrar_buses.short_description = "Buses asignados"

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ("placa", "marca", "modelo", "estado_bus")
    search_fields = ("placa", "marca", "modelo")
    list_filter = ("estado_bus",)
    ordering = ("placa",)


#@admin.register(Parada)
#class ParadaAdmin(admin.ModelAdmin):
#    list_display = ("nombre_parada", "direccion", "tipo_punto", "ruta")
#    search_fields = ("nombre_parada", "direccion", "tipo_punto")
#    list_filter = ("tipo_punto", "ruta")
#    ordering = ("nombre_parada",)
#    list_select_related = ("ruta",)


@admin.register(TipoEstado)
class TipoEstadoAdmin(admin.ModelAdmin):
    list_display = ("nombre_estado", "descripcion", "ruta")
    search_fields = ("nombre_estado", "descripcion")
    list_filter = ("ruta",)
    ordering = ("nombre_estado",)
    list_select_related = ("ruta",)
