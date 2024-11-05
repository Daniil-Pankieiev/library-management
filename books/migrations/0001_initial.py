# Generated by Django 5.1.3 on 2024-11-05 13:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Book",
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
                ("author", models.CharField(max_length=255)),
                ("published_date", models.DateField(blank=True, null=True)),
                ("isbn", models.CharField(max_length=13, unique=True)),
                ("pages", models.IntegerField(blank=True, null=True)),
                ("cover", models.URLField(blank=True, null=True)),
                ("language", models.CharField(max_length=64)),
                (
                    "added_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="books_added",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
