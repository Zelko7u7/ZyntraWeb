from rest_framework.routers import DefaultRouter
from .views import RutinaViewSet, EjercicioViewSet, EntrenamientoViewSet

router = DefaultRouter()
router.register(r'rutinas', RutinaViewSet)
router.register(r'ejercicios', EjercicioViewSet)
router.register(r'entrenamientos', EntrenamientoViewSet) 

urlpatterns = router.urls