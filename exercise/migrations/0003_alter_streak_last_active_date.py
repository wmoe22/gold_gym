# Generated by Django 5.0.4 on 2024-04-21 14:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0002_streak_last_active_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streak',
            name='last_active_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
