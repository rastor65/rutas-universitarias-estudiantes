from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParadaViewSet

router = DefaultRouter()
router.register(r"", ParadaViewSet, basename="parada")

urlpatterns = [
    path("", include(router.urls)),
]
