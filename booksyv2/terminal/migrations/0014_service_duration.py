# Generated by Django 5.2 on 2025-05-27 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("terminal", "0013_remove_service_duration_remove_service_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="duration",
            field=models.IntegerField(default=60, help_text="Duration in minutes"),
        ),
    ]
