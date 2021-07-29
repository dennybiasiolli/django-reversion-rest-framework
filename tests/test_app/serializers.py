from django.contrib.auth.models import User
from rest_framework import serializers
from reversion.models import Revision, Version
from reversion_rest_framework.serializers import (
    RevisionSerializer,
    VersionSerializer,
)

from .models import TestModel


class TestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestModel
        fields = ['id', 'name']


class UserSerializer(serializers.Serializer):

    class Meta:
        model = User
        fields = ['username']


class CustomRevisionSerializer(RevisionSerializer):
    user = UserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )


class CustomVersionSerializer(VersionSerializer):
    revision = CustomRevisionSerializer(read_only=True)
