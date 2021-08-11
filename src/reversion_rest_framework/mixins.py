from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from reversion.models import Version

from .serializers import VersionSerializer


class HistoryModelMixin:
    version_model = None
    version_serializer = VersionSerializer

    def _get_version_model(self):
        if self.version_model:
            return self.version_model
        serializer_class = self.get_serializer_class()
        if issubclass(serializer_class, ModelSerializer):
            return serializer_class.Meta.model

    @action(detail=True, methods=['GET'], name='Get History')
    def history(self, request, pk=None):
        object = self.get_object()
        versions = Version.objects.get_for_object(object)
        serializer = self.version_serializer(versions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], name='Get Deleted')
    def deleted(self, request):
        versions = Version.objects.get_deleted(self._get_version_model())
        versions = versions.order_by('-revision__date_created')
        serializer = self.version_serializer(versions, many=True)
        return Response(serializer.data)
