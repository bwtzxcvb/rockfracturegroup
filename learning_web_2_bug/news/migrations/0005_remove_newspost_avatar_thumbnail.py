# Generated by Django 2.2.4 on 2019-09-15 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20190915_2005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newspost',
            name='avatar_thumbnail',
        ),
    ]