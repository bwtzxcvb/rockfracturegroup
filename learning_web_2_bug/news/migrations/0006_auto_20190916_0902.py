# Generated by Django 2.2.4 on 2019-09-16 01:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_remove_newspost_avatar_thumbnail'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newspost',
            options={'ordering': ('-createtime',)},
        ),
    ]
