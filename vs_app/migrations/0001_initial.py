# Generated by Django 3.0 on 2019-12-03 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AAVSOdata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, default=None, max_length=33, null=True)),
                ('AUID', models.CharField(blank=True, default=None, max_length=33, null=True)),
                ('RA2000', models.FloatField()),
                ('Declination2000', models.FloatField()),
                ('ProperMotionRA', models.FloatField(blank=True, default=None, null=True)),
                ('ProperMotionDec', models.FloatField(blank=True, default=None, null=True)),
                ('VariabilityType', models.CharField(blank=True, default=None, max_length=13, null=True)),
                ('Period', models.FloatField(blank=True, default=None, null=True)),
                ('Epoch', models.FloatField(blank=True, default=None, null=True)),
                ('MaxMag', models.FloatField(blank=True, default=None, null=True)),
                ('MinMag', models.FloatField(blank=True, default=None, null=True)),
                ('MaxMinMagFilter', models.CharField(blank=True, default=None, max_length=3, null=True)),
                ('SpectralType', models.CharField(blank=True, default=None, max_length=33, null=True)),
                ('Category', models.CharField(blank=True, default=None, max_length=15, null=True)),
                ('OID', models.CharField(blank=True, default=None, max_length=15, null=True)),
                ('Constellation', models.CharField(blank=True, default=None, max_length=9, null=True)),
            ],
            options={
                'index_together': {('RA2000', 'Declination2000')},
            },
        ),
        migrations.CreateModel(
            name='AstroMetryJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_number', models.PositiveIntegerField()),
                ('url', models.URLField()),
                ('orientation', models.FloatField(blank=True, default=None, null=True)),
                ('pixscale', models.FloatField(blank=True, default=None, null=True)),
                ('radius', models.FloatField(blank=True, default=None, null=True)),
                ('center_ra', models.FloatField()),
                ('center_dec', models.FloatField()),
            ],
            options={
                'index_together': {('center_ra', 'center_dec')},
            },
        ),
        migrations.CreateModel(
            name='SimbadData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MAIN_ID', models.CharField(blank=True, default=None, max_length=33, null=True)),
                ('RA', models.CharField(max_length=13)),
                ('DEC', models.CharField(max_length=13)),
                ('RA_PREC', models.IntegerField(blank=True, default=None, null=True)),
                ('COO_ERR_MAJA', models.FloatField(blank=True, default=None, null=True)),
                ('COO_ERR_MINA', models.FloatField(blank=True, default=None, null=True)),
                ('COO_ERR_ANGLE', models.FloatField(blank=True, default=None, null=True)),
                ('COO_QUAL', models.CharField(blank=True, default=None, max_length=3, null=True)),
                ('COO_WAVELENGTH', models.CharField(blank=True, default=None, max_length=3, null=True)),
                ('COO_BIBCODE', models.BinaryField(blank=True, default=None, max_length=21, null=True)),
            ],
            options={
                'index_together': {('RA', 'DEC')},
            },
        ),
        migrations.CreateModel(
            name='NewFits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naxis', models.IntegerField(blank=True, default=None, null=True)),
                ('naxis1', models.IntegerField(blank=True, default=None, null=True)),
                ('naxis2', models.IntegerField(blank=True, default=None, null=True)),
                ('date_obs', models.DateField()),
                ('ut_start', models.TimeField()),
                ('exptime', models.FloatField(blank=True, default=None, null=True)),
                ('ref_point_ra', models.FloatField()),
                ('ref_point_dec', models.FloatField()),
                ('ref_point_x', models.FloatField(blank=True, default=None, null=True)),
                ('ref_point_y', models.FloatField(blank=True, default=None, null=True)),
                ('tranform_matrix', models.FloatField(blank=True, default=None, null=True)),
                ('scale', models.FloatField(blank=True, default=None, null=True)),
                ('astro_job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vs_app.AstroMetryJob')),
            ],
            options={
                'index_together': {('ref_point_ra', 'ref_point_dec')},
            },
        ),
        migrations.CreateModel(
            name='CorrFits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_x', models.FloatField(blank=True, default=None, null=True)),
                ('field_y', models.FloatField(blank=True, default=None, null=True)),
                ('field_ra', models.FloatField()),
                ('field_dec', models.FloatField()),
                ('index_x', models.FloatField(blank=True, default=None, null=True)),
                ('index_y', models.FloatField(blank=True, default=None, null=True)),
                ('index_ra', models.FloatField(blank=True, default=None, null=True)),
                ('index_dec', models.FloatField(blank=True, default=None, null=True)),
                ('index_id', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('field_id', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('match_weight', models.FloatField(blank=True, default=None, null=True)),
                ('FLUX', models.FloatField(blank=True, default=None, null=True)),
                ('BACKGROUND', models.FloatField(blank=True, default=None, null=True)),
                ('aavso_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vs_app.AAVSOdata')),
                ('astro_job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vs_app.AstroMetryJob')),
                ('simbad_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vs_app.SimbadData')),
            ],
            options={
                'index_together': {('field_ra', 'field_dec')},
            },
        ),
    ]