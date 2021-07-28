from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from reversion.models import Version

from .serializers import VersionSerializer


class HistoryModelViewSet(ModelViewSet):
    @action(detail=True, methods=['GET'], name='Get History')
    def history(self, request, pk=None):
        object = self.get_object()
        versions = Version.objects.get_for_object(object)
        serializer = VersionSerializer(versions, many=True)
        return Response(serializer.data)
