from rest_framework.routers import DefaultRouter
from .views import RutaViewSet, BusViewSet, TipoEstadoViewSet



router = DefaultRouter()
router.register(r'rutas', RutaViewSet)
router.register(r'buses', BusViewSet)
router.register(r'tipos_estado', TipoEstadoViewSet) 

urlpatterns = router.urls