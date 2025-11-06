# backend/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from accounts.views import HealthCheckView



#hola

urlpatterns = [
    # Admin y estado del sistema
    path("admin/", admin.site.urls),
    path("health/", HealthCheckView.as_view(), name="healthcheck"),

    # Apps principales
    path("api/accounts/", include("accounts.urls")),
    path("api/gestion-cupo/", include("gestion_cupo.urls")),
    path('api/rutas/', include("rutas.urls")),
    path('api/gps/', include('gps.urls')),

    # Documentación OpenAPI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
