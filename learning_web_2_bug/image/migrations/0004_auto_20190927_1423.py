# Generated by Django 2.2.4 on 2019-09-27 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0003_auto_20190923_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='title',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='article.ArticlePost'),
        ),
    ]
