# Generated by Django 2.0.8 on 2019-01-04 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0002_auto_20190103_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='languagebase',
            name='version',
            field=models.CharField(default='0', help_text='版本', max_length=20, verbose_name='版本'),
        ),
    ]