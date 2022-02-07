from rest_framework import permissions
from reversion_rest_framework.viewsets import HistoryModelViewSet

from .models import TestModel, TestLimitedModel, TestParentModel
from .pagination import MyPageNumberPagination
from .serializers import (
    CustomVersionSerializer,
    TestModelSerializer,
    ParentTestModelSerializer,
    TestLimitedModelSerializer,
)


class TestModelViewSet(HistoryModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = TestModel.objects.all()
    serializer_class = TestModelSerializer
    permission_classes = [permissions.IsAuthenticated]


class TestModelCustomSerializerViewSet(HistoryModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = TestModel.objects.all()
    serializer_class = TestModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    version_serializer = CustomVersionSerializer


class TestModelPaginatedViewSet(HistoryModelViewSet):
    """
    API endpoint that allows pagination.
    """
    queryset = TestModel.objects.all()
    serializer_class = TestModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MyPageNumberPagination


class TestParentModelViewSet(HistoryModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = TestParentModel.objects.all()
    serializer_class = ParentTestModelSerializer
    permission_classes = [permissions.IsAuthenticated]

class TestLimitedModelViewSet(HistoryModelViewSet):
    """
    API endpoint that registers only `name` field in history.
    """
    queryset = TestLimitedModel.objects.all()
    serializer_class = TestLimitedModelSerializer
    permission_classes = [permissions.IsAuthenticated]
