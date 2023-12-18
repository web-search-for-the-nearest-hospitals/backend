from django.urls import include, path
from rest_framework.routers import DefaultRouter

from user.views import AuthView, UserTokenView, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet)

authpatterns = [
    path('signup/', AuthView.as_view()),
    path('token/', UserTokenView.as_view()),
]

urlpatterns = [
    path('auth/', include(authpatterns)),
    path('', include(router.urls)),
]