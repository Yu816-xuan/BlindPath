# Generated by Django 5.1.2 on 2024-11-06 07:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Monitor",
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
                ("location", models.CharField(max_length=255)),
                (
                    "latitude",
                    models.DecimalField(decimal_places=6, max_digits=9, null=True),
                ),
                (
                    "longitude",
                    models.DecimalField(decimal_places=6, max_digits=9, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Alarm",
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
                ("alarm_time", models.DateTimeField(auto_now_add=True)),
                (
                    "obstacle_type",
                    models.CharField(
                        choices=[
                            ("unknown", "未知"),
                            ("vehicle", "车辆"),
                            ("person", "行人"),
                            ("other", "其他"),
                        ],
                        default="unknown",
                        max_length=50,
                    ),
                ),
                ("is_processed", models.BooleanField(default=False)),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "monitor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="alarms",
                        to="myapp.monitor",
                    ),
                ),
            ],
        ),
    ]
