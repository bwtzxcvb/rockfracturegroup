# Generated by Django 2.2.4 on 2019-09-24 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0009_articlepost_article_writer'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepost',
            name='person_likes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
