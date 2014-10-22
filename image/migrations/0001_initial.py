# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0001_initial'),
        ('plot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoundingBox',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('w', models.IntegerField()),
                ('h', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(max_length=255)),
                ('channel', models.IntegerField(null=True)),
                ('focus', models.IntegerField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImageTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('rx', models.CharField(max_length=255)),
                ('reverse', models.CharField(max_length=255)),
                ('experiment', models.ForeignKey(related_name=b'image_template', to='control.Experiment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ModifiedImage',
            fields=[
                ('image_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='image.Image')),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=('image.image',),
        ),
        migrations.CreateModel(
            name='CellImage',
            fields=[
                ('modifiedimage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='image.ModifiedImage')),
                ('cell_instance', models.ForeignKey(related_name=b'images', to='control.CellInstance')),
            ],
            options={
            },
            bases=('image.modifiedimage',),
        ),
        migrations.CreateModel(
            name='PlotImage',
            fields=[
                ('modifiedimage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='image.ModifiedImage')),
                ('plot', models.ForeignKey(related_name=b'images', to='plot.Plot')),
            ],
            options={
            },
            bases=('image.modifiedimage',),
        ),
        migrations.AddField(
            model_name='modifiedimage',
            name='image',
            field=models.ForeignKey(related_name=b'modified', to='image.Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imagetemplate',
            name='image',
            field=models.OneToOneField(related_name=b'image_template', null=True, to='image.Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='image',
            name='experiment',
            field=models.ForeignKey(related_name=b'images', to='control.Experiment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='image',
            name='series',
            field=models.ForeignKey(related_name=b'images', to='control.Series'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='image',
            name='timestep',
            field=models.ForeignKey(related_name=b'images', to='control.Timestep'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='boundingbox',
            name='image',
            field=models.OneToOneField(related_name=b'bounding_box', to='image.ModifiedImage'),
            preserve_default=True,
        ),
    ]
