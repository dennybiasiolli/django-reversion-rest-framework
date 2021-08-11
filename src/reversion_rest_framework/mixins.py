from rest_framework import status
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
    
    @action(detail=True, methods=["PUT"], name="Revert State")
    def revert(self, request, *args, **kwargs):
        version_id = request.data.get("version_id", None)
        if not version_id:
            return Response(
                {"error": "Invalid Version Id"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        version = (
            Version.objects.get_for_object(self.get_object())
            .filter(pk=version_id)
            .first()
        )
        if not version:
            return Response(
                {"error": "Version Not Found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            version.revision.revert()
        except Exception as e:
            return Response(
                {"error": "Reverting Failed", "msg": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.version_serializer(version)
        return Response(serializer.data)
