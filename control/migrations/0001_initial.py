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
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CellInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position_x', models.IntegerField()),
                ('position_y', models.IntegerField()),
                ('position_z', models.IntegerField()),
                ('velocity_x', models.IntegerField()),
                ('velocity_y', models.IntegerField()),
                ('velocity_z', models.IntegerField()),
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
                ('base_path', models.CharField(max_length=255)),
                ('input_path', models.CharField(max_length=255)),
                ('output_path', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Extension',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('length', models.DecimalField(max_digits=6, decimal_places=4)),
                ('cell', models.ForeignKey(related_name=b'extensions', to='control.Cell')),
                ('cell_instance', models.ForeignKey(related_name=b'extensions', to='control.CellInstance')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.IntegerField()),
                ('experiment', models.ForeignKey(related_name=b'regions', to='control.Experiment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.IntegerField()),
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
                ('index', models.IntegerField()),
                ('experiment', models.ForeignKey(related_name=b'timesteps', to='control.Experiment')),
                ('series', models.ForeignKey(related_name=b'timesteps', to='control.Series')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='cellinstance',
            name='region',
            field=models.ForeignKey(related_name=b'cell_instances', to='control.Region'),
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
            name='series',
            field=models.ForeignKey(related_name=b'cells', to='control.Series'),
            preserve_default=True,
        ),
    ]
