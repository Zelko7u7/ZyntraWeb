from rest_framework.routers import DefaultRouter
from .views import PlanNutricionalViewSet, RegistroComidaViewSet
router = DefaultRouter()
router.register(r'plannutricional', PlanNutricionalViewSet)
router.register(r'registrocomida', RegistroComidaViewSet)

urlpatterns = router.urls