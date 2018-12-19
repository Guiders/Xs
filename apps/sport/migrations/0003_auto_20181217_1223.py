# Generated by Django 2.0.8 on 2018-12-17 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0002_auto_20181217_0702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='imgCover',
            field=models.CharField(default='', help_text='封面图', max_length=200, verbose_name='封面图'),
        ),
        migrations.AlterField(
            model_name='action',
            name='imgLocal',
            field=models.CharField(default='', help_text='本地地址', max_length=200, verbose_name='本地地址'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='imgCover',
            field=models.CharField(default='', help_text='封面图', max_length=200, verbose_name='封面图'),
        ),
        migrations.AlterField(
            model_name='program',
            name='imgCover',
            field=models.CharField(default='', help_text='封面图', max_length=200, verbose_name='封面图'),
        ),
    ]