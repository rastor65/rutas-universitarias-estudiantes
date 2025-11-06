from rest_framework.routers import DefaultRouter

from .views import GPSPosicionViewSet, EventoDesvioViewSet


router = DefaultRouter()
router.register(r'posiciones', GPSPosicionViewSet, basename='posicion')
router.register(r'eventos_desvio', EventoDesvioViewSet, basename='evento_desvio')

urlpatterns = router.urls
