from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AppointmentViewSet, OrganizationViewSet, SpecialtyViewSet,
                    TownViewSet)

app_name = 'api'
router = DefaultRouter()
router.register('organizations', OrganizationViewSet,
                basename='organizations')
router.register('specialties', SpecialtyViewSet)
router.register('towns', TownViewSet)
router.register('appointments', AppointmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
