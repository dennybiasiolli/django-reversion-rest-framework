import reversion
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError, transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from reversion.errors import RevertError, RevisionManagementError
from reversion.models import Version

from .serializers import VersionSerializer

REVISION_FILTER_FIELDS = {
    "date_created": "revision__date_created",
    "date_created__gt": "revision__date_created__gt",
    "date_created__gte": "revision__date_created__gte",
    "date_created__lt": "revision__date_created__lt",
    "date_created__lte": "revision__date_created__lte",
    "user": "revision__user",
}


class BaseHistoryMixin:
    version_serializer = VersionSerializer

    def _filter_version_queryset(self, request, queryset):
        """Filter a Version queryset using revision-related query parameters."""
        for param, lookup in REVISION_FILTER_FIELDS.items():
            value = request.query_params.get(param)
            if value is not None:
                queryset = queryset.filter(**{lookup: value})
        return queryset

    def _build_serializer(
        self, instance_class: type, queryset: QuerySet, many: bool = False
    ):
        """
        Wraps the original serializer within the Version serializer
        on the field_dict field.
        """

        class _InstanceSerializer(ModelSerializer):
            class Meta:
                model = instance_class
                fields = "__all__"

        class _VersionsSerializer(self.version_serializer):
            field_dict = SerializerMethodField()

            @staticmethod
            def get_field_dict(obj):
                model_serializer = _InstanceSerializer(data=obj.field_dict)
                try:
                    model_serializer.is_valid(raise_exception=True)
                    original_serializer = self.get_serializer(
                        model_serializer.validated_data
                    )
                    return original_serializer.data
                except (
                    ValidationError,
                    TypeError,
                    ValueError,
                    AttributeError,
                    KeyError,
                ):
                    return obj.field_dict

        return _VersionsSerializer(queryset, many=many)


class HistoryMixin(BaseHistoryMixin):
    @action(detail=True, methods=["GET"], name="Get History")
    def history(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        versions = Version.objects.get_for_object(instance)
        versions = self._filter_version_queryset(request, versions)
        versions = versions.order_by("-revision__date_created")
        page = self.paginate_queryset(versions)
        if page is not None:
            serializer = self._build_serializer(instance.__class__, page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self._build_serializer(instance.__class__, versions, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["GET"],
        name="Get Historic Version",
        url_path=r"history/(?P<version_pk>\d+)",
    )
    def version(self, request, pk=None, version_pk=None, *args, **kwargs):
        instance = self.get_object()
        version = get_object_or_404(
            Version.objects.get_for_object(instance), id=version_pk
        )
        serializer = self._build_serializer(instance.__class__, version)
        return Response(serializer.data)


class DeletedMixin(BaseHistoryMixin):
    version_model = None

    def _get_version_model(self):
        if self.version_model:
            return self.version_model
        serializer_class = self.get_serializer_class()
        if issubclass(serializer_class, ModelSerializer):
            return serializer_class.Meta.model

    def get_deleted_versions(self):
        """
        Return the deleted versions visible to the current request.

        Deleted objects are no longer in the database, so `get_queryset()`
        can't scope them. django-reversion doesn't record deletions: the
        deleted version is the object's last saved one. By default only
        objects last saved by the requesting user are returned. Override to
        widen or narrow it,
        e.g. `return Version.objects.get_deleted(self._get_version_model())`
        for viewsets where every user may see every deleted record.
        """
        user = self.request.user
        if not user.is_authenticated:
            return Version.objects.none()
        model = self._get_version_model()
        return Version.objects.get_deleted(model).filter(revision__user=user)

    @action(detail=False, methods=["GET"], name="Get Deleted")
    def deleted(self, request, *args, **kwargs):
        model = self._get_version_model()
        versions = self.get_deleted_versions()
        versions = self._filter_version_queryset(request, versions)
        versions = versions.order_by("-revision__date_created")
        page = self.paginate_queryset(versions)
        if page is not None:
            serializer = self._build_serializer(model, page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self._build_serializer(model, versions, many=True)
        return Response(serializer.data)


class RestoreMixin(DeletedMixin):
    @action(
        detail=False,
        methods=["POST"],
        name="Restore Deleted",
        url_path=r"restore/(?P<version_pk>\d+)",
    )
    def restore(self, request, version_pk=None, *args, **kwargs):
        """Restore a deleted model instance from a version."""
        version = self.get_deleted_versions().filter(pk=version_pk).first()
        if not version:
            return Response(
                {"error": "Version Not Found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            with transaction.atomic(using=version.db):
                version.revision.revert()
                # The restored object must be reachable through get_queryset(),
                # otherwise the restore is rolled back.
                try:
                    instance = self.get_queryset().get(pk=version.object_id)
                except ObjectDoesNotExist:
                    transaction.set_rollback(True, using=version.db)
                    return Response(
                        {"error": "Version Not Found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                with reversion.create_revision():
                    instance.save()
                    reversion.set_user(request.user)
                    reversion.set_comment(f"Restored from version {version_pk}")
        except (
            RevertError,
            RevisionManagementError,
            DatabaseError,
        ) as e:
            return Response(
                {"error": "Restoring Failed", "msg": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RevertMixin(HistoryMixin):
    @action(
        detail=True,
        methods=["POST"],
        name="Revert Version",
        url_path=r"revert/(?P<version_pk>\d+)",
    )
    def revert(self, request, pk=None, version_pk=None, *args, **kwargs):
        instance = self.get_object()
        versions = Version.objects.get_for_object_reference(instance, pk)
        version = versions.filter(pk=version_pk).first()
        if not version:
            return Response(
                {"error": "Version Not Found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            version.revision.revert()
            instance.refresh_from_db()
            with reversion.create_revision():
                instance.save()
                reversion.set_user(request.user)
                reversion.set_comment(f"Reverted to version {version_pk}")
        except (
            RevertError,
            RevisionManagementError,
            DatabaseError,
            ObjectDoesNotExist,
        ) as e:
            return Response(
                {"error": "Reverting Failed", "msg": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self._build_serializer(instance.__class__, version)
        return Response(serializer.data)
