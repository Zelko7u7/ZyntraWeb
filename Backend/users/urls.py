from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, AvatarViewSet, RegisterView
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'avatars', AvatarViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
] + router.urls