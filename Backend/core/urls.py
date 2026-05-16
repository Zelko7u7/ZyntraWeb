from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from users.views import CustomLoginView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls')),
    path('api/users/', include('users.urls')),
    path('api/workouts/', include('workouts.urls')),
    path('api/nutrition/', include('nutrition.urls')),
    path('api/progress/', include('progress.urls')),
    path('api/achievements/', include('achievements.urls')),
    path('api/chat/', include('chat.urls')),

    path('api/token/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)