# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagetemplate',
            name='image',
        ),
        migrations.AlterField(
            model_name='boundingbox',
            name='h',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='boundingbox',
            name='w',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='boundingbox',
            name='x',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='boundingbox',
            name='y',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='image',
            name='channel',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='image',
            name='file_name',
            field=models.CharField(default=b'file_name', max_length=255),
        ),
        migrations.AlterField(
            model_name='image',
            name='focus',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='imagetemplate',
            name='experiment',
            field=models.ForeignKey(related_name=b'image_templates', to='control.Experiment'),
        ),
        migrations.AlterField(
            model_name='imagetemplate',
            name='reverse',
            field=models.CharField(default=b'reverse', max_length=255),
        ),
        migrations.AlterField(
            model_name='imagetemplate',
            name='rx',
            field=models.CharField(default=b'rx', max_length=255),
        ),
    ]
