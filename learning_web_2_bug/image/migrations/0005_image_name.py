# Generated by Django 2.2.4 on 2019-09-27 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0004_auto_20190927_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='name',
            field=models.CharField(default=0, max_length=300),
            preserve_default=False,
        ),
    ]
