from rest_framework.routers import DefaultRouter
from .views import NivelViewSet, RangoViewSet, ProgresoViewSet

router = DefaultRouter()
router.register(r'nivel', NivelViewSet)
router.register(r'rango', RangoViewSet)
router.register(r'progreso', ProgresoViewSet)

urlpatterns = router.urls