# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-07 08:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hdata', '0005_auto_20171007_1645'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ljsecondchengjiaorecord',
            options={'verbose_name': '链家二手房成交记录'},
        ),
        migrations.AlterField(
            model_name='ljsecondchengjiaorecord',
            name='subarea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hdata.SubArea'),
        ),
        migrations.RemoveField(
            model_name='ljsecondchengjiaorecord',
            name='area',
        ),
        migrations.AlterUniqueTogether(
            name='ljsecondchengjiaorecord',
            unique_together=set([('unit_price', 'title', 'deal_date', 'total_price')]),
        ),
    ]
