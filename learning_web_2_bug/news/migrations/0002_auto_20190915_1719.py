# Generated by Django 2.2.4 on 2019-09-15 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newspost',
            old_name='news_tage',
            new_name='news_tag',
        ),
    ]