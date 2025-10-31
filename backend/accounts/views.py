from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import ScopedRateThrottle
from accounts.permissions import HasRoleResourcePermission
from rest_framework.permissions import IsAuthenticated
from accounts.audit import AuditMixin

from .models import Role, Resource
from .serializers import (
    RegisterSerializer, UserSerializer, RoleSerializer, ResourceSerializer,
    PasswordChangeSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer
)


    
from .models import UserActivityLog, Permission
from .serializers import UserActivityLogSerializer, PermissionSerializer

User = get_user_model()

class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)

@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfInitView(APIView):
    """
    GET -> setea cookie 'csrftoken' para que el front pueda enviar X-CSRFToken.
    Útil cuando el frontend es SPA en otro origen.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"detail": "CSRF cookie set"}, status=status.HTTP_200_OK)

class SessionLoginView(AuditMixin, APIView):
    """
    POST {username, password, remember_me?}
    Crea sesión (cookie 'sessionid'). Requiere X-CSRFToken.
    - remember_me=true => sesión ~14 días
    - remember_me=false => expira al cerrar el navegador
    """
    permission_classes = [AllowAny]
    throttle_scope = "auth_login"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request):
        username = (request.data.get("username") or "").strip()
        password = request.data.get("password") or ""
        remember = bool(request.data.get("remember_me"))

        if not username or not password:
            return Response({"detail": "Faltan credenciales."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"detail": "Credenciales inválidas."}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            return Response({"detail": "Usuario inactivo."}, status=status.HTTP_403_FORBIDDEN)

        login(request, user)

        request.session.set_expiry(60 * 60 * 24 * 14 if remember else 0)

        return Response({
            "detail": "Sesión iniciada",
            "remember_me": remember,
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)

class SessionLogoutView(AuditMixin, APIView):
    """
    POST sin cuerpo -> cierra sesión (elimina cookie 'sessionid').
    Requiere X-CSRFToken porque modifica estado.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "Sesión cerrada"}, status=status.HTTP_200_OK)

class MeSessionView(APIView):
    """
    GET -> devuelve el usuario autenticado por sesión.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

class PasswordChangeView(AuditMixin, APIView):
    """
    POST {old_password, new_password}
    Cambia la contraseña del usuario autenticado (por sesión).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = PasswordChangeSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({"detail": "Contraseña cambiada"}, status=status.HTTP_200_OK)

class RegisterView(AuditMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Registro básico. Por seguridad, NO auto-login aquí (flujo explícito de login).
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.none()
    http_method_names = ["post"]

class PasswordResetRequestView(AuditMixin, APIView):
    """
    POST {email[, base_url]}
    Envía enlace de recuperación. Devuelve sent=True/False.
    (Throttle específico para evitar abuso.)
    """
    permission_classes = [AllowAny]
    throttle_scope = "password_reset"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request):
        ser = PasswordResetRequestSerializer(
            data=request.data,
            context={"request": request, "base_url": request.data.get("base_url")}
        )
        ser.is_valid(raise_exception=True)
        result = ser.save()
        if result.get("found"):
            return Response({"detail": "Correo de recuperación enviado.", "sent": True}, status=status.HTTP_200_OK)
        return Response({"detail": "No se encontró un usuario con ese email.", "sent": False}, status=status.HTTP_404_NOT_FOUND)

class PasswordResetConfirmView(AuditMixin, APIView):
    """
    POST {uid, token, new_password}
    Confirma el restablecimiento y establece la nueva contraseña.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        ser = PasswordResetConfirmSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({"detail": "Contraseña restablecida correctamente."}, status=status.HTTP_200_OK)

class UserViewSet(AuditMixin, viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("date_joined")
    serializer_class = UserSerializer
    permission_classes = [HasRoleResourcePermission]
    required_scopes = ["users.read"]

    def get_required_scopes(self):
        if self.request.method in ("POST", "PUT", "PATCH", "DELETE"):
            return ["users.write"]
        return self.required_scopes

    def get_permissions(self):
        self.required_scopes = self.get_required_scopes()
        return super().get_permissions()


class RoleViewSet(AuditMixin, viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by("name")
    serializer_class = RoleSerializer
    permission_classes = [HasRoleResourcePermission]
    required_scopes = ["roles.read"]

    def get_required_scopes(self):
        if self.request.method in ("POST", "PUT", "PATCH", "DELETE"):
            return ["roles.write"]
        if getattr(self, "action", "") in ("assign_users", "assign_resources"):
            return ["roles.write"]
        return self.required_scopes

    def get_permissions(self):
        self.required_scopes = self.get_required_scopes()
        return super().get_permissions()

    @action(detail=True, methods=["post"])
    def assign_users(self, request, pk=None):
        role = self.get_object()
        ids = request.data.get("user_ids", [])
        if not isinstance(ids, list):
            return Response({"detail": "user_ids debe ser una lista."}, status=status.HTTP_400_BAD_REQUEST)
        users = User.objects.filter(id__in=ids)
        role.users.add(*users)
        return Response({"assigned": [str(u.id) for u in users]}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def assign_resources(self, request, pk=None):
        role = self.get_object()
        resource_ids = request.data.get("resource_ids", [])
        if not isinstance(resource_ids, list):
            return Response({"detail": "resource_ids debe ser una lista."}, status=status.HTTP_400_BAD_REQUEST)
        resources = Resource.objects.filter(id__in=resource_ids)
        role.resources.add(*resources)
        return Response({"assigned": [str(r.id) for r in resources]}, status=status.HTTP_200_OK)

class ResourceViewSet(AuditMixin, viewsets.ModelViewSet):
    queryset = Resource.objects.all().order_by("name")
    serializer_class = ResourceSerializer
    permission_classes = [HasRoleResourcePermission]
    required_scopes = ["resources.read"]

    def get_required_scopes(self):
        if self.request.method in ("POST", "PUT", "PATCH", "DELETE"):
            return ["resources.write"]
        return self.required_scopes

    def get_permissions(self):
        self.required_scopes = self.get_required_scopes()
        return super().get_permissions()

class ProfileUpdateView(AuditMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Devuelve el perfil actual"""
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        """Actualiza el perfil"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class UserActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vista de solo lectura (GET list/retrieve) para registros de actividad.
    Permite a administradores o usuarios autorizados auditar acciones del sistema.
    """
    queryset = UserActivityLog.objects.select_related("user").all()
    serializer_class = UserActivityLogSerializer
    permission_classes = [HasRoleResourcePermission]
    required_scopes = ["activitylogs.read"]

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            return self.queryset.filter(user=user)
        return self.queryset

    def get_required_scopes(self):
        return self.required_scopes

class PermissionViewSet(AuditMixin, viewsets.ModelViewSet):
    """
    CRUD completo para la gestión de permisos personalizados.
    Relaciona permisos con recursos del sistema.
    """
    queryset = Permission.objects.prefetch_related("resources").all()
    serializer_class = PermissionSerializer
    permission_classes = [HasRoleResourcePermission]
    required_scopes = ["permissions.read"]

    def get_required_scopes(self):
        if self.request.method in ("POST", "PUT", "PATCH", "DELETE"):
            return ["permissions.write"]
        return self.required_scopes

    def get_permissions(self):
        self.required_scopes = self.get_required_scopes()
        return super().get_permissions()
