# Generated by Django 3.0 on 2019-12-12 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vs_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aavsodata',
            name='MaxMag',
            field=models.CharField(blank=True, default=None, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='aavsodata',
            name='MinMag',
            field=models.CharField(blank=True, default=None, max_length=15, null=True),
        ),
    ]
