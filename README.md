# django-reversion-rest-framework

A package for adding a django-reversion history endpoint to django-rest-framework ModelViewSet.


## Configuration

Follow the official website for the installation and the integration of django-reversion in your project, otherwise future steps won't work.

You might need to enable the `ReversionMiddleware` for storing a version for each API change.<br>
Follow the instructions [here](https://django-reversion.readthedocs.io/en/stable/middleware.html),
you should add `'reversion.middleware.RevisionMiddleware'` to your `MIDDLEWARE` setting.


### Using the HistoryModelViewSet

The `HistoryModelViewSet` extends django-rest-framework's `ModelViewSet`
adding a GET `history` action in the detail,
displaying a list of all revisions of that specific record.

You can use the `HistoryModelViewSet` in place of the `ModelViewSet`
during viewsets definition.

```py
from reversion_rest_framework.viewsets import HistoryModelViewSet


class MyModelViewSet(HistoryModelViewSet):
    # ...
```

Then if your endpoint exposes on the url `/my-models/` you can get the history
of a record using `my-models/<pk>/history/`.
