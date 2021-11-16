import reversion
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from reversion.models import Version

from .serializers import VersionSerializer


class BaseHistoryModelMixin:
    version_serializer = VersionSerializer


class HistoryOnlyMixin(BaseHistoryModelMixin):
    @action(detail=True, methods=['GET'], name='Get History')
    def history(self, request, pk=None):
        instance = self.get_object()
        versions = Version.objects.get_for_object(instance).order_by(
            '-revision__date_created'
        )
        page = self.paginate_queryset(versions)
        if page is not None:
            serializer = self.version_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.version_serializer(versions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], name='Get Historic Version', url_path=r'history/(?P<version_pk>\d+)')
    def version(self, request, pk=None, version_pk=None):
        instance = self.get_object()
        version = get_object_or_404(Version.objects.get_for_object(instance), id=version_pk)
        serializer = self.version_serializer(version)
        return Response(serializer.data)


class DeletedOnlyMixin(BaseHistoryModelMixin):
    version_model = None

    def _get_version_model(self):
        if self.version_model:
            return self.version_model
        serializer_class = self.get_serializer_class()
        if issubclass(serializer_class, ModelSerializer):
            return serializer_class.Meta.model

    @action(detail=False, methods=['GET'], name='Get Deleted')
    def deleted(self, request):
        versions = Version.objects.get_deleted(self._get_version_model())
        versions = versions.order_by('-revision__date_created')
        serializer = self.version_serializer(versions, many=True)
        return Response(serializer.data)


class ReadOnlyHistoryModel(HistoryOnlyMixin, DeletedOnlyMixin):
    pass


class RevertMixin(HistoryOnlyMixin):
    @action(detail=True, methods=['POST'], name='Revert Version',
            url_path='revert/(?P<version_pk>\d+)')
    def revert(self, request, pk=None, version_pk=None, *args, **kwargs):
        if not version_pk:
            return Response(
                {'error': 'Invalid Version Id'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance = self.get_object()
        versions = Version.objects.get_for_object_reference(instance, pk)
        version = versions.filter(pk=version_pk).first()
        if not version:
            return Response(
                {'error': 'Version Not Found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            version.revision.revert()
            instance.refresh_from_db()
            with reversion.create_revision():
                instance.save()
                reversion.set_user(request.user)
                reversion.set_comment(
                    'Reverted to version {}'.format(version_pk))
        except Exception as e:
            return Response(
                {'error': 'Reverting Failed', 'msg': str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.version_serializer(version)
        return Response(serializer.data)


class HistoryModelMixin(RevertMixin, DeletedOnlyMixin):
    pass
