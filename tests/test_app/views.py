from rest_framework import viewsets
from rest_framework import permissions

from .models import TestModel
from .serializers import TestModelSerializer


class TestModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = TestModel.objects.all()
    serializer_class = TestModelSerializer
    permission_classes = [permissions.IsAuthenticated]
