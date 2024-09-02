from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser, PermissionsMixin


class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    country = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.name}, {self.country}"


class Airports(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    city = models.ForeignKey(City, related_name='airports', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.city.name})"


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    regular_place_price = models.DecimalField(max_digits=10, decimal_places=2)
    additional_leg_space_price = models.DecimalField(max_digits=10, decimal_places=2)
    near_window_price = models.DecimalField(max_digits=10, decimal_places=2)
    no_meal_price = models.DecimalField(max_digits=10, decimal_places=2)
    basic_meal_price = models.DecimalField(max_digits=10, decimal_places=2)
    premium_meal_price = models.DecimalField(max_digits=10, decimal_places=2)
    internet_service_price = models.DecimalField(max_digits=10, decimal_places=2)
    entertainment_service_price = models.DecimalField(max_digits=10, decimal_places=2)
    power_socket_service_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class AirplaneType(models.Model):
    id = models.AutoField(primary_key=True)
    model_name = models.CharField(max_length=40)
    base_seats = models.IntegerField()
    premium_seats = models.IntegerField()
    business_seats = models.IntegerField()
    business_rows = models.IntegerField(default=0)
    first_class_rows = models.IntegerField(default=0)
    economy_rows = models.IntegerField(default=0)
    seats_per_business_row = models.IntegerField(default=4)
    seats_per_first_class_row = models.IntegerField(default=2)
    seats_per_economy_row = models.IntegerField(default=6)

    def __str__(self):
        return self.model_name


class Airplane(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(AirplaneType, related_name='airplanes', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='airplanes', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.type.model_name} - {self.id}"


class Discount(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.IntegerField()

    def __str__(self):
        return f"Discount {self.value}%"


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    payment = models.FloatField(default=0)
    discount_id = models.ForeignKey(Discount, related_name='orders', on_delete=models.SET(None))

    def __str__(self):
        return f"Order {self.id}"


class Passenger(models.Model):
    GENDER_CHOICES = [
        ('F', 'Female'),
        ('M', 'Male'),
        ('U', 'Undisclosed'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    sur_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')

    def __str__(self):
        return f"{self.name} {self.sur_name}"


class Meal(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    price = models.FloatField()

    def __str__(self):
        return self.name


class OnboardService(models.Model):
    name = models.CharField(max_length=50)
    id = models.AutoField(primary_key=True)
    price = models.FloatField()

    def __str__(self):
        return self.name


class Baggage(models.Model):
    id = models.AutoField(primary_key=True)
    height = models.FloatField(default=0)
    width = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    number = models.FloatField(default=0)
    price = models.IntegerField(default=0)


class HandLuggage(models.Model):
    id = models.AutoField(primary_key=True)
    height = models.FloatField(default=0)
    width = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    number = models.FloatField(default=0)
    price = models.IntegerField(default=0)


class AdditionalServices(models.Model):
    id = models.AutoField(primary_key=True)
    meal = models.ForeignKey(Meal, on_delete=models.SET_NULL, null=True)
    services = models.ManyToManyField(OnboardService)
    baggage = models.ForeignKey(Baggage, null=True, related_name="service", on_delete=models.SET_NULL)
    hand_luggage = models.ForeignKey(Baggage, null=True, related_name="services", on_delete=models.SET_NULL)

    def __str__(self):
        return f" Meal: {self.meal}"


class Seat(models.Model):
    CLASS_CHOICES = [
        ('EC', 'Economy'),
        ('BC', 'Business'),
        ('FC', 'First Class'),
    ]

    flight_class = models.CharField(max_length=2, choices=CLASS_CHOICES)
    flight_id = models.ForeignKey('Flight', related_name='seats', on_delete=models.CASCADE)
    passenger_id = models.ForeignKey('Passenger', related_name='seat', on_delete=models.SET(None), default=None,
                                     null=True)
    number = models.CharField(max_length=4)
    booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('flight_id', 'number')

    def __str__(self):
        return f"Seat {self.number} - {self.flight_class}"


class Flight(models.Model):
    id = models.AutoField(primary_key=True)
    arrival_airport = models.ForeignKey(Airports, related_name='arrival_flights', on_delete=models.SET(None))
    departure_airport = models.ForeignKey(Airports, related_name='departure_flights', on_delete=models.SET(None))
    destination = models.ForeignKey(City, related_name='destination_flights', on_delete=models.SET(None))
    origin = models.ForeignKey(City, related_name='origin_flights', on_delete=models.SET(None))
    airplane = models.ForeignKey(Airplane, related_name='flights', on_delete=models.SET(None))
    date_of_flight = models.DateTimeField()
    arriving_date = models.DateTimeField()
    economy_seat_price = models.FloatField(default=0)
    first_seat_price = models.FloatField(default=0)
    business_seat_price = models.FloatField(default=0)
    available_meal = models.ManyToManyField(Meal, related_name='flight_meal')
    available_luggage = models.ManyToManyField(HandLuggage, related_name='flight_luggage')
    available_baggage = models.ManyToManyField(Baggage, related_name='flight_baggage')
    available_services = models.ManyToManyField(OnboardService, related_name="flight_services")

    def __str__(self):
        return f"Flight {self.id} - {self.departure_airport.name} to {self.arrival_airport.name}"


class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    seat_id = models.OneToOneField(Seat, related_name='ticket', on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, related_name='tickets', on_delete=models.CASCADE)
    services = models.OneToOneField(AdditionalServices, related_name='ticket', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Ticket {self.id}"


class MyUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **extra_fields)


class MyUser(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    object = MyUserManager
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'




