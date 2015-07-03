# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Town',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('county', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('description', models.TextField()),
                ('max_temperature', models.FloatField()),
                ('min_temperature', models.FloatField()),
                ('wind_speed', models.IntegerField(verbose_name='wind speed', validators=[django.core.validators.MinValueValidator(0)])),
                ('precipitation', models.IntegerField(verbose_name='precipitation')),
                ('precipitation_probability', models.IntegerField(verbose_name='precipitation probability', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('observations', models.TextField(verbose_name='weather observations')),
                ('town', models.ForeignKey(related_name='town', to='ExportingFiles.Town')),
            ],
        ),
    ]
