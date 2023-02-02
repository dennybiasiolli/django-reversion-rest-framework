# Generated by Django 3.2.9 on 2021-11-17 09:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("test_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TestParentModel",
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
                ("children", models.ManyToManyField(to="test_app.TestModel")),
            ],
        ),
    ]
