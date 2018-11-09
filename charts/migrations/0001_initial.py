# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-11-09 05:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChartType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35, verbose_name='图表类型')),
            ],
            options={
                'verbose_name': '图表类型',
                'verbose_name_plural': '图表类型',
            },
        ),
        migrations.CreateModel(
            name='ComposeIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='图表名称')),
                ('data_src', models.CharField(max_length=200, verbose_name='数据源表')),
                ('procedure', models.CharField(blank=True, max_length=200, null=True, verbose_name='过滤条件')),
                ('chart_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='charts.ChartType', verbose_name='图表类型')),
            ],
            options={
                'verbose_name': '仪表盘',
                'verbose_name_plural': '仪表盘',
            },
        ),
        migrations.CreateModel(
            name='DataSetField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=100, verbose_name='字段名称')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='转换名称')),
                ('field_type', models.CharField(choices=[('dis', 'dis'), ('mst', 'mst')], max_length=100, verbose_name='字段类型')),
            ],
            options={
                'verbose_name': '数据集字段表',
                'verbose_name_plural': '数据集字段表',
            },
        ),
        migrations.CreateModel(
            name='MeasurementType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='类型')),
                ('value', models.CharField(max_length=100, verbose_name='表达式')),
            ],
            options={
                'verbose_name': '度量聚合类型',
                'verbose_name_plural': '度量聚合类型',
            },
        ),
        migrations.AddField(
            model_name='datasetfield',
            name='mst_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='charts.MeasurementType', verbose_name='度量聚合'),
        ),
        migrations.AddField(
            model_name='composeindex',
            name='dis',
            field=models.ManyToManyField(related_name='dis', to='charts.DataSetField', verbose_name='维度'),
        ),
        migrations.AddField(
            model_name='composeindex',
            name='mst',
            field=models.ManyToManyField(related_name='mst', to='charts.DataSetField', verbose_name='度量'),
        ),
    ]
