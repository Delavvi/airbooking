# Generated by Django 5.0.7 on 2024-07-13 13:36

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(choices=[('RE', 'Regular'), ('AS', 'Additional leg space'), ('NW', 'Near window')], max_length=2)),
                ('meal', models.CharField(choices=[('NO', 'No meal'), ('RE', 'Basic meal'), ('VP', 'Premium meal')], max_length=2)),
                ('services', models.CharField(choices=[('internet', 'Access to internet'), ('entertainment', 'Access to entertainment system'), ('power_socket', 'Access to device powering')], default=None, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='AirplaneType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('model_name', models.CharField(max_length=40)),
                ('base_seats', models.IntegerField()),
                ('premium_seats', models.IntegerField()),
                ('business_seats', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('country', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('regular_place_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('additional_leg_space_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('near_window_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('no_meal_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('basic_meal_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('premium_meal_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('internet_service_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('entertainment_service_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('power_socket_service_price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('sur_name', models.CharField(max_length=20)),
                ('passport_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'User',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Airplane',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='airplanes', to='authentication.airplanetype')),
            ],
        ),
        migrations.CreateModel(
            name='Airports',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='airports', to='authentication.city')),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_of_flight', models.DateField()),
                ('arriving_date', models.DateField()),
                ('airplane', models.ForeignKey(on_delete=models.SET(None), related_name='flights', to='authentication.airplane')),
                ('arrival_airport', models.ForeignKey(on_delete=models.SET(None), related_name='arrival_flights', to='authentication.airports')),
                ('departure_airport', models.ForeignKey(on_delete=models.SET(None), related_name='departure_flights', to='authentication.airports')),
                ('destination', models.ForeignKey(on_delete=models.SET(None), related_name='destination_flights', to='authentication.city')),
                ('origin', models.ForeignKey(on_delete=models.SET(None), related_name='origin_flights', to='authentication.city')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('payment', models.FloatField(default=0)),
                ('discount_id', models.ForeignKey(on_delete=models.SET(None), related_name='orders', to='authentication.discount')),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('flight_class', models.CharField(choices=[('EC', 'Economy'), ('BC', 'Business'), ('FC', 'First Class')], max_length=2)),
                ('number', models.IntegerField()),
                ('type', models.CharField(choices=[('EC', 'Economy'), ('BC', 'Business'), ('FC', 'First Class')], max_length=2)),
                ('flight_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='authentication.flight')),
                ('passenger_id', models.ForeignKey(on_delete=models.SET(None), related_name='seats', to='authentication.passenger')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='authentication.company')),
                ('order_id', models.ForeignKey(on_delete=models.SET(None), related_name='tickets', to='authentication.order')),
                ('seat_id', models.OneToOneField(on_delete=models.SET(None), related_name='ticket', to='authentication.seat')),
                ('services', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ticket', to='authentication.additionalservices')),
            ],
        ),
    ]
