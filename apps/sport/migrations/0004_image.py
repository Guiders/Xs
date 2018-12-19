# Generated by Django 2.0.8 on 2018-12-17 13:52

import XServer.settings
from django.db import migrations, models
import sport.models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0003_auto_20181217_1223'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imgType', models.IntegerField(choices=[(1, '普通封面图'), (2, '视频封面')], help_text='图片类型', verbose_name='图片类型')),
                ('img', models.ImageField(storage=XServer.settings.ImageStorage(), upload_to=sport.models.Image.get_photo_path)),
            ],
            options={
                'verbose_name': '图片',
                'verbose_name_plural': '图片',
                'db_table': 'sport_image',
            },
        ),
    ]
