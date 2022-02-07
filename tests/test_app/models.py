from django.db import models
import reversion


@reversion.register()
class TestModel(models.Model):
    name = models.CharField(max_length=10)


@reversion.register()
class TestParentModel(models.Model):
    children = models.ManyToManyField(TestModel)


@reversion.register(fields=('name',))
class TestLimitedModel(models.Model):
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
