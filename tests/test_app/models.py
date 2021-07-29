from django.db import models
import reversion


@reversion.register()
class TestModel(models.Model):
    name = models.CharField(max_length=10)
