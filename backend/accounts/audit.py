from accounts.models import UserActivityLog


class AuditMixin:
    """
    Mixin para registrar automáticamente operaciones CRUD en UserActivityLog.
    Debe colocarse antes de GenericViewSet o ModelViewSet.
    """

    audit_action_prefix = None  # ejemplo: "rutas" o "cupos"

    def _registrar_log(self, request, action, descripcion=None):
        if not request.user or not request.user.is_authenticated:
            return

        UserActivityLog.objects.create(
            user=request.user,
            action=action,
            description=descripcion or "",
            ip_address=getattr(request, "client_ip", None),
            device=getattr(request, "user_agent", None),
        )

    def perform_create(self, serializer):
        instance = serializer.save()
        if self.audit_action_prefix:
            self._registrar_log(
                self.request,
                f"{self.audit_action_prefix}.create",
                f"Creó {instance}",
            )

    def perform_update(self, serializer):
        instance = serializer.save()
        if self.audit_action_prefix:
            self._registrar_log(
                self.request,
                f"{self.audit_action_prefix}.update",
                f"Actualizó {instance}",
            )

    def perform_destroy(self, instance):
        if self.audit_action_prefix:
            self._registrar_log(
                self.request,
                f"{self.audit_action_prefix}.delete",
                f"Eliminó {instance}",
            )
        instance.delete()
