# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cellinstance',
            name='max_z',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cellinstance',
            name='min_z',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='experiment',
            name='name',
            field=models.CharField(default=b'name', max_length=255),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='experiment',
            name='x_microns_over_pixels',
            field=models.DecimalField(default=0.0, max_digits=6, decimal_places=4),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='experiment',
            name='y_microns_over_pixels',
            field=models.DecimalField(default=0.0, max_digits=6, decimal_places=4),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='experiment',
            name='z_microns_over_pixels',
            field=models.DecimalField(default=0.0, max_digits=6, decimal_places=4),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cellinstance',
            name='position_x',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='cellinstance',
            name='position_y',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='cellinstance',
            name='position_z',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='cellinstance',
            name='velocity_x',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='cellinstance',
            name='velocity_y',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='cellinstance',
            name='velocity_z',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='base_path',
            field=models.CharField(default=b'base_path', max_length=255),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='input_path',
            field=models.CharField(default=b'input_path', max_length=255),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='output_path',
            field=models.CharField(default=b'output_path', max_length=255),
        ),
        migrations.AlterField(
            model_name='extension',
            name='length',
            field=models.DecimalField(default=0.0, max_digits=6, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='region',
            name='index',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='series',
            name='index',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='timestep',
            name='index',
            field=models.IntegerField(default=0),
        ),
    ]
