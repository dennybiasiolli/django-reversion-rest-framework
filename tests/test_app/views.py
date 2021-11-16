from rest_framework import permissions
from reversion_rest_framework.viewsets import HistoryModelViewSet

from .models import TestModel
from .pagination import MyPageNumberPagination
from .serializers import CustomVersionSerializer, TestModelSerializer


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
