# Generated by Django 5.2 on 2025-06-09 04:07

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Company",
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
                ("company_name", models.CharField(max_length=100)),
                ("company_email", models.EmailField(max_length=254, unique=True)),
                ("industry", models.CharField(max_length=50)),
                ("company_size", models.CharField(max_length=20)),
                ("password", models.CharField(max_length=128)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Register",
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
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=100, unique=True)),
                ("password", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Intro",
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
                ("full_name", models.CharField(max_length=100)),
                ("tagline", models.CharField(blank=True, max_length=200)),
                ("about_me", models.TextField(blank=True)),
                ("location", models.CharField(blank=True, max_length=100)),
                (
                    "profile_picture",
                    models.ImageField(blank=True, null=True, upload_to="profile_pics/"),
                ),
                (
                    "resume",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="resumes/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["pdf", "doc", "docx"],
                                message="Please upload a valid document file (PDF, DOC, or DOCX).",
                            )
                        ],
                    ),
                ),
                ("email", models.EmailField(blank=True, max_length=100)),
                ("phone", models.CharField(blank=True, max_length=20)),
                ("linkedin", models.URLField(blank=True)),
                ("github", models.URLField(blank=True)),
                ("twitter", models.URLField(blank=True)),
                ("website", models.URLField(blank=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="intro",
                        to="myportfolio.register",
                    ),
                ),
            ],
            options={
                "verbose_name": "Portfolio Introduction",
                "verbose_name_plural": "Portfolio Introductions",
            },
        ),
    ]
