from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import OrganizationViewSet, SpecialtyViewSet

app_name = 'api'
router = DefaultRouter()
router.register('organizations', OrganizationViewSet,
                basename='organizations')
router.register('specialties', SpecialtyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
