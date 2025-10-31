from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from math import radians, cos, sin, sqrt, atan2

from .models import (
    User,
    Role,
    Resource,
    UserRole,
    RoleResource,
    UserActivityLog,
    Permission,
)


# === FUNCIONES DE APOYO ===
def haversine_distance(lat1, lon1, lat2, lon2):
    """Calcula la distancia en kilómetros entre dos coordenadas GPS."""
    if None in [lat1, lon1, lat2, lon2]:
        return None
    R = 6371  # Radio de la Tierra en km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


# === FILTRO PERSONALIZADO POR PROXIMIDAD GPS ===
class NearbyUserFilter(admin.SimpleListFilter):
    title = _("Usuarios cercanos a una ubicación")
    parameter_name = "gps_proximity"

    def lookups(self, request, model_admin):
        return [
            ("uniguajira", _("Cerca de la Universidad (Riohacha)")),
            ("custom", _("Coordenadas personalizadas")),
        ]

    def queryset(self, request, queryset):
        if self.value() == "uniguajira":
            # Coordenadas aproximadas del campus principal
            base_lat, base_lon = 11.5446, -72.9060
            max_distance_km = 3  # radio de 3 km
            nearby_ids = []
            for user in queryset:
                if user.gps_latitude and user.gps_longitude:
                    dist = haversine_distance(
                        base_lat, base_lon, float(user.gps_latitude), float(user.gps_longitude)
                    )
                    if dist is not None and dist <= max_distance_km:
                        nearby_ids.append(user.id)
            return queryset.filter(id__in=nearby_ids)
        return queryset


# === INLINES ===
class UserRoleInline(admin.TabularInline):
    model = UserRole
    extra = 0
    autocomplete_fields = ["role"]
    readonly_fields = ["assigned_at"]


class RoleResourceInline(admin.TabularInline):
    model = RoleResource
    extra = 0
    autocomplete_fields = ["resource"]
    readonly_fields = ["granted_at"]


# === ADMIN PERSONALIZADOS ===
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Campos adicionales que no interfieren con los del modelo base
    fieldsets = (
        (_("Credenciales"), {"fields": ("username", "password")}),
        (_("Información personal"), {"fields": ("first_name", "last_name", "email", "phone", "avatar")}),
        (_("Estado"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Permisos"), {"fields": ("groups", "user_permissions")}),
        (_("Información de ubicación y conexión"), {
            "fields": (
                "gps_latitude",
                "gps_longitude",
                "verified_email",
                "is_active_gps",
                "last_connection",
            ),
        }),
        (_("Fechas importantes"), {"fields": ("last_login", "date_joined")}),
    )

    # Campos que se muestran al crear un nuevo usuario
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "email",
                "first_name",
                "last_name",
                "phone",
                "avatar",
                "password1",
                "password2",
                "identificacion",
                "is_active",
            ),
        }),
    )

    list_display = (
        "username",
        "email",
        "phone",
        "is_staff",
        "verified_email",
        "gps_latitude",
        "gps_longitude",
        "last_connection",
    )
    list_filter = ("is_staff", "is_active", "verified_email", NearbyUserFilter)
    search_fields = ("username", "email", "first_name", "last_name", "phone")
    ordering = ("username",)
    inlines = [UserRoleInline]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "description")
    search_fields = ("name", "slug")
    inlines = [RoleResourceInline]


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ( "name", "link_frontend", "link_backend", "description", "icon" )
    search_fields = ("name", "link_frontend", "link_backend")
    list_filter = ("roles",)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "assigned_at")
    list_filter = ("role",)
    search_fields = ("user__username", "role__name")
    readonly_fields = ("assigned_at",)


@admin.register(RoleResource)
class RoleResourceAdmin(admin.ModelAdmin):
    list_display = ("role", "resource", "granted_at")
    list_filter = ("role",)
    search_fields = ("role__name", "resource__name")
    readonly_fields = ("granted_at",)


@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ("user", "action", "ip_address", "device", "created_at")
    search_fields = ("user__username", "action", "device", "ip_address")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "description")
    search_fields = ("code", "name")
    filter_horizontal = ("resources",)
