from rest_framework.routers import DefaultRouter
from .views import ChatConversacionViewSet, ChatMensajeViewSet

router = DefaultRouter()
router.register(r'chatconversacion', ChatConversacionViewSet)
router.register(r'chatmensaje', ChatMensajeViewSet)

urlpatterns = router.urls