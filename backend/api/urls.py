from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AppointmentViewSet, OrganizationViewSet,
                    SpecialtyViewSet, TownViewSet, )
from .views.auth import SignUp, LoginView

app_name = 'api'
router = DefaultRouter()
router.register('organizations', OrganizationViewSet,
                basename='organizations')
router.register('specialties', SpecialtyViewSet)
router.register('towns', TownViewSet,
                basename='towns')
router.register('appointments', AppointmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', SignUp.as_view()),
    path('login/', LoginView.as_view(), name="login"),
]
