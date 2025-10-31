# accounts/permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import Resource, Permission


class HasRoleResourcePermission(BasePermission):
    """
    Permiso avanzado basado en Roles, Recursos y Permisos.
    Evalúa:
      1️⃣ Si el usuario está autenticado.
      2️⃣ Si tiene algún rol que incluya el recurso (link_backend).
      3️⃣ Si posee el permiso necesario (view, create, update, delete) sobre ese recurso.
    """

    def has_permission(self, request, view):
        user = request.user

        # --- 1️⃣ Verificación de autenticación ---
        if not user or not user.is_authenticated:
            return False

        # --- 2️⃣ Superusuario: acceso total ---
        if getattr(user, "is_superuser", False):
            return True

        path = (request.path or "").lower().strip()
        if not path.endswith("/"):
            path += "/"

        # --- 3️⃣ Determinar acción solicitada ---
        action = self._map_method_to_permission(request.method)
        if not action:
            return False  # método HTTP no reconocido

        # --- 4️⃣ Buscar recursos asociados al usuario ---
        user_resources = Resource.objects.filter(roles__users=user).distinct()

        # --- 5️⃣ Evaluar acceso por recurso y permiso ---
        for resource in user_resources:
            link = (resource.link_backend or "").strip().lower()
            if not link:
                continue
            if not link.endswith("/"):
                link += "/"

            # Coincidencia de ruta (path inicia con el link del recurso)
            if path.startswith(link):
                # Si no hay permisos asociados al recurso, permitir por defecto
                if not resource.permissions.exists():
                    return True

                # Buscar permisos asociados al recurso
                resource_perms = Permission.objects.filter(resources=resource)
                # Ejemplo: code = "rutas.view" o "cupos.create"
                for perm in resource_perms:
                    code = perm.code.lower()
                    if code.endswith(f".{action}"):
                        return True

        return False

    # --- 🔧 Helper: mapear método HTTP a tipo de permiso ---
    def _map_method_to_permission(self, method: str) -> str:
        method = method.upper()
        if method in SAFE_METHODS:      # GET, HEAD, OPTIONS
            return "view"
        if method == "POST":
            return "create"
        if method in ("PUT", "PATCH"):
            return "update"
        if method == "DELETE":
            return "delete"
        return ""
