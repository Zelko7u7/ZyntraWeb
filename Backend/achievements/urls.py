from rest_framework.routers import DefaultRouter
from .views import LogroViewSet, LogroUsuarioViewSet

router = DefaultRouter()
router.register(r'logro', LogroViewSet)
router.register(r'logrousuario', LogroUsuarioViewSet)

urlpatterns = router.urls