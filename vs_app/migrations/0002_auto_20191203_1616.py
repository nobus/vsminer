# Generated by Django 3.0 on 2019-12-03 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vs_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='astrometryjob',
            name='id',
        ),
        migrations.AlterField(
            model_name='astrometryjob',
            name='job_number',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
    ]