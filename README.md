# django-reversion-rest-framework

A package for adding a django-reversion history endpoint to django-rest-framework ModelViewSet.


## Configuration

Follow the official website for the installation and the integration of django-reversion in your project, otherwise future steps won't work.

You might need to enable the `ReversionMiddleware` for storing a version for each API change.<br>
Follow the instructions [here](https://django-reversion.readthedocs.io/en/stable/middleware.html),
you should add `'reversion.middleware.RevisionMiddleware'` to your `MIDDLEWARE` setting.


### Using the HistoryModelViewSet

The `HistoryModelViewSet` extends django-rest-framework's `ModelViewSet` adding

- a GET `history` action in the detail

    displaying a list of all revisions of that specific record

- a GET `deleted` action in the list

    displaying a list of all deleted records

You can use the `HistoryModelViewSet` in place of the `ModelViewSet`
during viewsets definition.

```py
from reversion_rest_framework.viewsets import HistoryModelViewSet


class MyModelViewSet(HistoryModelViewSet):
    # ...
```

Then if your endpoint exposes on the url `/my-models/` you can get

- the history of a record using `my-models/<pk>/history/`

- all deleted records (ordered by date_created descending) using `my-models/deleted/`


### Customizing the VersionSerializer

The `HistoryModelViewSet` comes up with a `history` action using a `VersionSerializer`.<br>
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
