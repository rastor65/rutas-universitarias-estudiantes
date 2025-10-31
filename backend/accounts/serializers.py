# accounts/serializers.py

from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from rest_framework import serializers
from .models import Role, Resource, UserActivityLog, Permission

User = get_user_model()

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ["id", "name", "description"]

class RoleSerializer(serializers.ModelSerializer):
    resources = ResourceSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ["id", "name", "slug", "description", "resources"]

class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "avatar",
            "first_name",
            "last_name",
            "username",
            "email",
            "is_active",
            "is_staff",
            "roles"
        ]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(required=True, max_length=50)
    last_name = serializers.CharField(required=True, max_length=50)
    email = serializers.EmailField(required=True)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = User
        fields = [
            "id",
            "avatar",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "is_active",
        ]

    def validate_email(self, value):
        email = (value or "").strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("Ya existe un usuario con este correo.")
        return email

    def validate_password(self, value):
        from django.contrib.auth import password_validation
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data["email"] = validated_data["email"].strip().lower()
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError({"old_password": _("Contraseña actual incorrecta")})
        password_validation.validate_password(attrs["new_password"], user)
        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return (value or "").strip().lower()

    def save(self):
        """
        Devuelve {'found': True/False}. Si found=True, envía email HTML con botón.
        """
        request = self.context.get("request")
        email = self.validated_data["email"]

        qs = User.objects.filter(email__iexact=email, is_active=True)
        if not qs.exists():
            return {"found": False}

        user = qs.first()
        uid = urlsafe_base64_encode(smart_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        base_url = self.context.get("base_url")
        if base_url:
            reset_url = f"{base_url}?uid={uid}&token={token}"
        else:
            path = reverse("password_reset_confirm")
            if request is not None:
                reset_url = request.build_absolute_uri(f"{path}?uid={uid}&token={token}")
            else:
                reset_url = f"http://localhost:8000{path}?uid={uid}&token={token}"

        brand = {
            "app_name": getattr(settings, "APP_DISPLAY_NAME", "Gestión Hotelera"),
            "support_email": getattr(settings, "SUPPORT_EMAIL", "soporte@hotel.local"),
            "primary_color": getattr(settings, "BRAND_PRIMARY_COLOR", "#0ea5e9"),
            "logo_url": getattr(settings, "BRAND_LOGO_URL", None),
        }

        subject = "Recuperación de contraseña"
        text_body = (
            f"Hola {user.username},\n\n"
            f"Recibimos una solicitud para restablecer tu contraseña en {brand['app_name']}.\n"
            f"Para continuar, abre el siguiente enlace:\n{reset_url}\n\n"
            "Si no fuiste tú, puedes ignorar este mensaje.\n"
            f"— Equipo {brand['app_name']}\n"
        )
        html_body = render_to_string(
            "email/password_reset.html",
            {"user": user, "reset_url": reset_url, **brand},
        )

        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@hotel.local")
        msg = EmailMultiAlternatives(subject, text_body, from_email, [email])
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=True)

        return {"found": True}

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        uid = attrs.get("uid")
        token = attrs.get("token")
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id, is_active=True)
        except Exception:
            raise serializers.ValidationError({"uid": _("Token inválido o usuario no encontrado.")})

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError({"token": _("Token inválido o expirado.")})

        password_validation.validate_password(attrs["new_password"], user)
        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user

class UserActivityLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = UserActivityLog
        fields = ["id", "user", "action", "description", "ip_address", "device", "created_at"]

class PermissionSerializer(serializers.ModelSerializer):
    resources = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Resource.objects.all())

    class Meta:
        model = Permission
        fields = ["id", "code", "name", "description", "resources"]


__all__ = [
    "ResourceSerializer",
    "RoleSerializer",
    "UserSerializer",
    "RegisterSerializer",
    "PasswordChangeSerializer",
    "PasswordResetRequestSerializer",
    "PasswordResetConfirmSerializer",
]
