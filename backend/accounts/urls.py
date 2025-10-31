from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import (
    UserViewSet,
    RoleViewSet,
    ResourceViewSet,
    PermissionViewSet,
    UserActivityLogViewSet,
    CsrfInitView,
    SessionLoginView,
    SessionLogoutView,
    MeSessionView,
    ProfileUpdateView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"roles", RoleViewSet, basename="roles")
router.register(r"resources", ResourceViewSet, basename="resources")
router.register(r"permissions", PermissionViewSet, basename="permissions")
router.register(r"activity-logs", UserActivityLogViewSet, basename="activitylogs")

urlpatterns = [
    # --- Autenticación y sesión ---
    path("auth/csrf/", CsrfInitView.as_view(), name="csrf_init"),
    path("auth/login/", SessionLoginView.as_view(), name="session_login"),
    path("auth/logout/", SessionLogoutView.as_view(), name="session_logout"),
    path("auth/me/", MeSessionView.as_view(), name="session_me"),
    path("auth/me/update/", ProfileUpdateView.as_view(), name="profile_update"),

    # --- Recuperación de contraseña ---
    path("auth/password/reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path("auth/password/reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    # --- Rutas del router DRF ---
    path("", include(router.urls)),
]
