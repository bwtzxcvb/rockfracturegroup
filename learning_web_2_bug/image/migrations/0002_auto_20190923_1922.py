# Generated by Django 2.2.4 on 2019-09-23 11:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ('-publish',)},
        ),
        migrations.AddField(
            model_name='image',
            name='publish',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]