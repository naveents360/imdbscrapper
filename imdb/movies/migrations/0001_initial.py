# Generated by Django 5.1.5 on 2025-01-26 07:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Movie",
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
                ("title", models.CharField(max_length=255)),
                (
                    "year",
                    models.PositiveIntegerField(
                        blank=True,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(1800)],
                    ),
                ),
                ("rating", models.FloatField(blank=True, null=True)),
                ("director", models.CharField(blank=True, max_length=255, null=True)),
                ("cast", models.TextField(blank=True, null=True)),
                ("story", models.TextField(blank=True, null=True)),
                ("genre", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                "indexes": [
                    models.Index(fields=["genre"], name="movies_movi_genre_f96e97_idx")
                ],
                "unique_together": {("title", "year")},
            },
        ),
    ]
