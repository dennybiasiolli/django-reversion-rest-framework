# Generated manually for issue #141 regression test

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("test_app", "0003_testlimitedmodel"),
    ]

    operations = [
        migrations.CreateModel(
            name="TestUniqueModel",
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
                ("code", models.CharField(max_length=10, unique=True)),
                ("name", models.CharField(max_length=50)),
            ],
        ),
    ]
