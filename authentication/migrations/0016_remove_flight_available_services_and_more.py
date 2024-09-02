# Generated by Django 5.0.7 on 2024-08-12 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0015_remove_additionalservices_baggage_weight_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flight',
            name='available_services',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='base_business_class',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='base_economy',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='base_first_class',
        ),
        migrations.AddField(
            model_name='flight',
            name='available_baggage',
            field=models.ManyToManyField(related_name='flight_baggage', to='authentication.baggage'),
        ),
        migrations.AddField(
            model_name='flight',
            name='available_luggage',
            field=models.ManyToManyField(related_name='flight_luggage', to='authentication.handluggage'),
        ),
        migrations.AddField(
            model_name='flight',
            name='available_meal',
            field=models.ManyToManyField(related_name='flight_meal', to='authentication.meal'),
        ),
    ]
