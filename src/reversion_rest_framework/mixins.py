from typing import Optional

import reversion
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.fields import SerializerMethodField
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from reversion.models import Version

from .serializers import VersionSerializer


class BaseHistoryModelMixin:
    version_serializer = VersionSerializer


class HistoryOnlyMixin(BaseHistoryModelMixin):

    def _build_serializer(self, instance_class: type, queryset: QuerySet, many: Optional[bool] = False):
        """
            Wraps the original serializer within the Version serializer on the field_dict field
        """

        class _InstanceSerializer(ModelSerializer):

            class Meta:
                model = instance_class
                fields = '__all__'

        class _VersionsSerializer(self.version_serializer):
            field_dict = SerializerMethodField()

            @staticmethod
            def get_field_dict(obj):
                # here we use the transient ModelSerializer to serialize
                # the json blob returned from the version
                model_serializer = _InstanceSerializer(data=obj.field_dict)
                try:
                    model_serializer.is_valid(raise_exception=True)
                    # we now get the original serializer as specified by the user on the viewset,
                    # and use it to de-serializer the model-instance
                    original_serializer = self.get_serializer(model_serializer.validated_data)
                    return original_serializer.data
                except Exception:
                    return obj.field_dict

        return _VersionsSerializer(queryset, many=many)

    @action(detail=True, methods=['GET'], name='Get History')
    def history(self, request, pk=None):
        instance = self.get_object()
        versions = Version.objects.get_for_object(instance).order_by(
            '-revision__date_created'
        )
        page = self.paginate_queryset(versions)
        if page is not None:
            serializer = self._build_serializer(instance.__class__, page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self._build_serializer(instance.__class__, versions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], name='Get Historic Version', url_path=r'history/(?P<version_pk>\d+)')
    def version(self, request, pk=None, version_pk=None):
        instance = self.get_object()
        version = get_object_or_404(Version.objects.get_for_object(instance), id=version_pk)
        serializer = self._build_serializer(instance.__class__, version)
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
        model = self._get_version_model()
        versions = Version.objects.get_deleted(model)
        versions = versions.order_by('-revision__date_created')
        page = self.paginate_queryset(versions)
        if page is not None:
            serializer = self._build_serializer(model, page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self._build_serializer(model, versions, many=True)
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
        serializer = self._build_serializer(instance.__class__, version)
        return Response(serializer.data)


class HistoryModelMixin(RevertMixin, DeletedOnlyMixin):
    pass
