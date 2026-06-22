# Generated manually for issue #141 regression test (unique_together + FK)

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("test_app", "0004_testuniquemodel"),
    ]

    operations = [
        migrations.CreateModel(
            name="TestUniqueTogetherModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("category", models.CharField(max_length=10)),
                ("code", models.CharField(max_length=10)),
                ("name", models.CharField(max_length=50)),
                (
                    "related",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="test_app.testmodel",
                    ),
                ),
            ],
            options={
                "unique_together": {("category", "code")},
            },
        ),
    ]
