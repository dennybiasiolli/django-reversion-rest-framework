from django.contrib.auth.models import User
from rest_framework import serializers
from reversion_rest_framework.serializers import (
    RevisionSerializer,
    VersionSerializer,
)

from .models import TestModel, TestLimitedModel, TestParentModel


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


class ParentTestModelSerializer(serializers.ModelSerializer):
    """A crude nested writable serializer,
    good enough for this test with no dependency on a 3rd party package.
    """
    children = TestModelSerializer(many=True)

    def create_or_update(self, validated_data, instance=None):
        children = validated_data.pop('children')

        if instance is not None:
            this = super().update(instance, validated_data)
        else:
            this = super().create(validated_data)

        this.children.set([TestModel.objects.create(**child)
                          for child in children])
        this.save()
        return this

    def update(self, instance, validated_data):
        return self.create_or_update(validated_data, instance)

    def create(self, validated_data):
        return self.create_or_update(validated_data)

    class Meta:
        model = TestParentModel
        fields = ('id', 'children')

class TestLimitedModelSerializer(serializers.ModelSerializer):
    # description = serializers.CharField()

    class Meta:
        model = TestLimitedModel
        fields = ['id', 'name', 'description']
