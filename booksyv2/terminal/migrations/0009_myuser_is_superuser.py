# Generated by Django 5.2 on 2025-04-11 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("terminal", "0008_myuser_is_staff"),
    ]

    operations = [
        migrations.AddField(
            model_name="myuser",
            name="is_superuser",
            field=models.BooleanField(default=False),
        ),
    ]
