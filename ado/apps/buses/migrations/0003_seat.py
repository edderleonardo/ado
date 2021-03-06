# Generated by Django 3.2.9 on 2021-11-25 04:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('passengers', '0001_initial'),
        ('buses', '0002_remove_bus_route'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.IntegerField()),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='buses.bus')),
                ('passenger', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seats_passengers', to='passengers.passenger')),
            ],
        ),
    ]
