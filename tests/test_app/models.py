import reversion
from django.db import models


@reversion.register()
class TestModel(models.Model):  # noqa: DJ008
    name = models.CharField(max_length=10)


@reversion.register()
class TestParentModel(models.Model):  # noqa: DJ008
    children = models.ManyToManyField(TestModel)


@reversion.register(fields=("name",))
class TestLimitedModel(models.Model):  # noqa: DJ008
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
