from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TestLimitedModelViewSet,
    TestModelCustomSerializerViewSet,
    TestModelPaginatedViewSet,
    TestModelViewSet,
    TestParentModelViewSet,
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register("test-models", TestModelViewSet)
router.register(
    "test-models-custom", TestModelCustomSerializerViewSet, basename="testmodelcustom"
)
router.register(
    "test-models-paginated", TestModelPaginatedViewSet, basename="testmodelpaginated"
)
router.register(
    "test-parent-models", TestParentModelViewSet, basename="testparentmodel"
)
router.register(
    "test-limited-models", TestLimitedModelViewSet, basename="testlimitedmodel"
)


# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
]
