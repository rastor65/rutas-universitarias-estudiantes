from django.contrib import admin
from .models import GPSPosition, Route, Device, GPSEvent

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'activo', 'creado_en')
    search_fields = ('nombre',)
    list_filter = ('activo',)
    ordering = ('-creado_en',)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'imei', 'nombre', 'activo', 'creado_en', 'ultima_posicion')
    search_fields = ('imei', 'nombre')
    list_filter = ('activo',)
    ordering = ('-creado_en',)

@admin.register(GPSEvent)
class GPSEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'descripcion')
    search_fields = ('codigo',)

@admin.register(GPSPosition)
class GPSPositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_ruta', 'id_usuario', 'latitud', 'longitud', 'velocidad', 'fecha_hora')
    list_display_links = ('id', 'id_ruta')
    list_filter = ('id_ruta',)
    search_fields = ('id_usuario', 'id_ruta')
    ordering = ('-fecha_hora',)
    list_per_page = 50
    date_hierarchy = 'fecha_hora'
    readonly_fields = ('fecha_hora',)

    fieldsets = (
        (None, {
            'fields': ('id_ruta', 'id_usuario', ('latitud', 'longitud'), 'velocidad', 'id_evento', 'device')
        }),
        ('Geometría', {
            'fields': ('geom',),
        }),
        ('Lectura', {
            'fields': ('fecha_hora',),
        }),
    )

    # Inyectar DataTables en la página de lista para que se vea como una tabla interactiva
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            content = response.content.decode('utf-8')
            inject = """
<link rel="stylesheet" href="https://cdn.datatables.net/1.13.4/css/jquery.dataTables.min.css"/>
<script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
<script>
(function($){
    $(function(){
        var $tbl = $('#result_list');
        if ($tbl.length && ! $tbl.data('dt-initialized')) {
            try {
                $tbl.DataTable({
                    paging: true,
                    pageLength: 50,
                    lengthMenu: [10, 25, 50, 100],
                    order: [[6, 'desc']],
                    autoWidth: false,
                    language: {
                        url: "//cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json"
                    }
                });
                $tbl.data('dt-initialized', true);
            } catch (e) {
                console.warn('DataTables init falló', e);
            }
        }
    });
})(django.jQuery);
</script>
"""
            if '</body>' in content and 'cdn.datatables.net' not in content:
                content = content.replace('</body>', inject + '</body>')
                response.content = content.encode('utf-8')
        except Exception:
            pass
        return response
