# Generated by Django 3.2.9 on 2021-11-25 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buses', '0002_remove_bus_route'),
        ('routes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='buses',
            field=models.ManyToManyField(to='buses.Bus'),
        ),
    ]
