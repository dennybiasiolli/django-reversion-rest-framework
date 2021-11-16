from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TestModelViewSet,
    TestModelCustomSerializerViewSet,
    TestModelPaginatedViewSet,
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('test-models', TestModelViewSet)
router.register('test-models-custom', TestModelCustomSerializerViewSet,
                basename='testmodelcustom')
router.register('test-models-paginated', TestModelPaginatedViewSet,
                basename='testmodelpaginated')


# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
