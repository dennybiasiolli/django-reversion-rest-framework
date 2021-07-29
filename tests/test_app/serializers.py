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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CustomRevisionSerializer(RevisionSerializer):
    user = UserSerializer()


class CustomVersionSerializer(VersionSerializer):
    revision = CustomRevisionSerializer()
