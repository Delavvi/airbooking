# Generated by Django 5.0.7 on 2024-08-12 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0017_flight_available_services'),
    ]

    operations = [
        migrations.AddField(
            model_name='baggage',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='handluggage',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
