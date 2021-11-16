# django-reversion-rest-framework

A package for adding a django-reversion history endpoint to django-rest-framework ModelViewSet.


## Configuration

Follow the official website for the installation and the integration of django-reversion in your project, otherwise future steps won't work.

You might need to enable the `ReversionMiddleware` for storing a version for each API change.<br>
Follow the instructions [here](https://django-reversion.readthedocs.io/en/stable/middleware.html),
you should add `'reversion.middleware.RevisionMiddleware'` to your `MIDDLEWARE` setting.


### Using the HistoryModelViewSet

The `HistoryModelViewSet` extends django-rest-framework's `ModelViewSet` adding

- a GET `history` action in the detail (`/my-model-url/<pk>/history/`)

    displaying a list of all revisions of that specific record

- a GET `version` action in the history detail (`/my-model-url/<pk>/history/<version_pk>/`)

    displaying a specific revisions of that specific record

- a GET `deleted` action in the list (`/my-model-url/deleted/`)

    displaying a list of all deleted records

- a POST `revert` action in the detail (`/my-model-url/<pk>/revert/<version_pk>/`)

    allowing users to revert to a previous revision of the object

You can use the `HistoryModelViewSet` in place of the `ModelViewSet`
during viewsets definition.

```py
from reversion_rest_framework.viewsets import HistoryModelViewSet


class MyModelViewSet(HistoryModelViewSet):
    # ...
```

For advanced or selective implementation, you can use `reversion_rest_framework.mixins`.

- `HistoryOnlyMixin` contains `history` and `version` actions

- `DeletedOnlyMixin` contains only the `deleted` action

- `ReadOnlyHistoryModel` contains `history`, `version` and `deleted` actions

- `RevertMixin` contains `history`, `version` and `revert` actions


### Customizing the VersionSerializer

The `HistoryModelViewSet` comes up with actions using a `VersionSerializer`.<br>
To customize the serializer with one of your own, you can use `version_serializer`.<br>
For example, if you want to customize the `user` serializer inside a revision,
you can use the following code:

```py
from django.contrib.auth.models import User
from rest_framework import serializers
from reversion_rest_framework.viewsets import HistoryModelViewSet
from reversion.models import Revision, Version
from reversion_rest_framework.serializers import (
    RevisionSerializer,
    VersionSerializer,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CustomRevisionSerializer(RevisionSerializer):
    user = UserSerializer()


class CustomVersionSerializer(VersionSerializer):
    revision = CustomRevisionSerializer()


class MyModelViewSet(HistoryModelViewSet):
    version_serializer = CustomVersionSerializer
    # ...
```
