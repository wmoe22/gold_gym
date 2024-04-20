# Generated by Django 5.0.4 on 2024-04-17 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercises',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('bodyPart', models.CharField(max_length=200)),
                ('equipment', models.CharField(max_length=300)),
                ('gifUrl', models.URLField()),
                ('target', models.CharField(max_length=100)),
                ('secondaryMuscles', models.JSONField(default=list)),
                ('instructions', models.JSONField(default=list)),
            ],
        ),
    ]