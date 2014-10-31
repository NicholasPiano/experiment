# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CellInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('second_region', models.CharField(default=b'', max_length=1)),
                ('position_x', models.IntegerField(default=0)),
                ('position_y', models.IntegerField(default=0)),
                ('position_z', models.IntegerField(default=0)),
                ('velocity_x', models.IntegerField(default=0)),
                ('velocity_y', models.IntegerField(default=0)),
                ('velocity_z', models.IntegerField(default=0)),
                ('displacement_x', models.IntegerField(default=0)),
                ('displacement_y', models.IntegerField(default=0)),
                ('displacement_z', models.IntegerField(default=0)),
                ('volume', models.IntegerField(default=0)),
                ('surface_area', models.IntegerField(default=0)),
                ('cell', models.ForeignKey(related_name=b'cell_instances', to='control.Cell')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'name', max_length=255)),
                ('base_path', models.CharField(default=b'base_path', max_length=255)),
                ('input_path', models.CharField(default=b'input_path', max_length=255)),
                ('output_path', models.CharField(default=b'output_path', max_length=255)),
                ('x_microns_over_pixels', models.DecimalField(default=0.0, max_digits=6, decimal_places=4)),
                ('y_microns_over_pixels', models.DecimalField(default=0.0, max_digits=6, decimal_places=4)),
                ('z_microns_over_pixels', models.DecimalField(default=0.0, max_digits=6, decimal_places=4)),
                ('time_per_frame', models.DecimalField(default=0.0, max_digits=10, decimal_places=4)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Extension',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('length', models.DecimalField(default=0.0, max_digits=8, decimal_places=4)),
                ('angle', models.DecimalField(default=0.0, max_digits=8, decimal_places=4)),
                ('cell_instance', models.ForeignKey(related_name=b'extensions', to='control.CellInstance')),
                ('experiment', models.ForeignKey(related_name=b'extensions', to='control.Experiment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(default=b'region')),
                ('index', models.IntegerField(default=0)),
                ('experiment', models.ForeignKey(related_name=b'regions', default=None, to='control.Experiment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.IntegerField(default=0)),
                ('z0', models.IntegerField(default=0)),
                ('experiment', models.ForeignKey(related_name=b'series', to='control.Experiment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Timestep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.IntegerField(default=0)),
                ('experiment', models.ForeignKey(related_name=b'timesteps', to='control.Experiment')),
                ('series', models.ForeignKey(related_name=b'timesteps', to='control.Series')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='cellinstance',
            name='experiment',
            field=models.ForeignKey(related_name=b'cell_instances', to='control.Experiment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cellinstance',
            name='region',
            field=models.ForeignKey(related_name=b'cell_instances', to='control.Region'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cellinstance',
            name='series',
            field=models.ForeignKey(related_name=b'cell_instances', to='control.Series'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cellinstance',
            name='timestep',
            field=models.ForeignKey(related_name=b'cell_instances', to='control.Timestep'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cell',
            name='experiment',
            field=models.ForeignKey(related_name=b'cells', to='control.Experiment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cell',
            name='series',
            field=models.ForeignKey(related_name=b'cells', to='control.Series'),
            preserve_default=True,
        ),
    ]
