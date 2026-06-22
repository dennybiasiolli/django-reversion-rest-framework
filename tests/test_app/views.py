from rest_framework import permissions

from reversion_rest_framework.viewsets import HistoryModelViewSet

from .models import TestLimitedModel, TestModel, TestParentModel, TestUniqueModel
from .pagination import MyPageNumberPagination
from .serializers import (
    CustomVersionSerializer,
    ParentTestModelSerializer,
    TestLimitedModelSerializer,
    TestModelSerializer,
    TestUniqueModelSerializer,
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


class TestUniqueModelViewSet(HistoryModelViewSet):
    """
    API endpoint with a unique field and custom serializer representation.
    Regression for #141: serializer_class must apply even when the row exists.
    """

    queryset = TestUniqueModel.objects.all()
    serializer_class = TestUniqueModelSerializer
    permission_classes = [permissions.IsAuthenticated]
