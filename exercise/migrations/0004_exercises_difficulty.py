# Generated by Django 5.0.4 on 2024-04-19 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0003_progress_exercises_saved'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercises',
            name='difficulty',
            field=models.CharField(choices=[('easy', 'Easy'), ('medium', 'medium'), ('hard', 'Hard')], default='medium', max_length=10),
        ),
    ]