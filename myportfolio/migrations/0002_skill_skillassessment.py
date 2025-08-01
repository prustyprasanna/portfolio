# Generated by Django 5.2 on 2025-06-12 04:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myportfolio", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Skill",
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
                ("category", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="SkillAssessment",
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
                ("score", models.IntegerField()),
                ("completed_date", models.DateTimeField(auto_now_add=True)),
                ("verified", models.BooleanField(default=False)),
                (
                    "skill",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="myportfolio.skill",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="myportfolio.register",
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "skill")},
            },
        ),
    ]
