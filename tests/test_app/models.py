import reversion
from django.db import models


@reversion.register()
class TestModel(models.Model):
    name = models.CharField(max_length=10)


@reversion.register()
class TestParentModel(models.Model):
    children = models.ManyToManyField(TestModel)


@reversion.register(fields=("name",))
class TestLimitedModel(models.Model):
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=100)


@reversion.register()
class TestUniqueModel(models.Model):
    """Model with a unique field; reproduces issue #141."""

    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
