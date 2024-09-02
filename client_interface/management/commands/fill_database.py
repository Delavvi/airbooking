from faker import Faker
from django.db import transaction
from django.core.management.base import BaseCommand
from authentication.models import City, AirplaneType, Airports, Flight, Airplane, AdditionalServices, Meal
from authentication.models import HandLuggage, Baggage
from authentication.models import OnboardService
from datetime import datetime
import pytz


class Command(BaseCommand):
    help = 'Fill database with fake data'

    def handle(self, *args, **options):
        fake = Faker()
        fake.seed_instance(42)
        airplane_type = AirplaneType.objects.create(model_name='B1', base_seats=20, premium_seats=20, business_seats=20,
                                     business_rows=4, economy_rows=4, first_class_rows=4,
                                     seats_per_business_row=5, seats_per_first_class_row=5,
                                     seats_per_economy_row=5)
        airplane = Airplane.objects.create(type=airplane_type)
        for city in range(5):
            with transaction.atomic():
                city_name1 = fake.city()
                city_name2 = fake.city()
                city_object1 = City.objects.create(country=fake.country(), name=city_name1)
                city_object2 = City.objects.create(country=fake.country(), name=city_name2)
                airport1 = Airports.objects.create(name=f"{city_name1}_airport", city=city_object1)
                airport2 = Airports.objects.create(name=f"{city_name2}_airport", city=city_object2)
                timezone = pytz.UTC
                date_of_flight = datetime.strptime('10.10.2027 14:30', '%d.%m.%Y %H:%M').replace(tzinfo=timezone)
                arriving_date = datetime.strptime('10.10.2027 17:30', '%d.%m.%Y %H:%M').replace(tzinfo=timezone)
                meal1 = Meal.objects.create(name='Some food',
                                           price=fake.pyfloat(left_digits=2, right_digits=2, positive=True))
                on_board1 = OnboardService.objects.create(name='Wi-Fi', price=fake.pyfloat(left_digits=2))
                baggage1 = Baggage.objects.create(weight=10, height=20, width=20, number=2)
                hand_baggage1 = HandLuggage.objects.create(width=5, height=10, weight=5, number=1)
                meal2 = Meal.objects.create(name='Chicken Sandwich',
                                            price=fake.pyfloat(left_digits=2, right_digits=2, positive=True))
                on_board2 = OnboardService.objects.create(name='In-flight Entertainment',
                                                          price=fake.pyfloat(left_digits=2))
                baggage2 = Baggage.objects.create(weight=15, height=25, width=25, number=1)
                hand_baggage2 = HandLuggage.objects.create(width=7, height=12, weight=7, number=2)
                meal3 = Meal.objects.create(name='Vegetarian Pasta',
                                            price=fake.pyfloat(left_digits=2, right_digits=2, positive=True))
                on_board3 = OnboardService.objects.create(name='Extra Legroom', price=fake.pyfloat(left_digits=2))
                baggage3 = Baggage.objects.create(weight=20, height=30, width=30, number=3)
                hand_baggage3 = HandLuggage.objects.create(width=10, height=15, weight=8, number=1)
                flight = Flight.objects.create(
                    arrival_airport=airport1,
                    departure_airport=airport2,
                    destination=city_object1,
                    origin=city_object2,
                    airplane=airplane,
                    date_of_flight=date_of_flight,
                    arriving_date=arriving_date,
                )
                flight.available_meal.add(meal1, meal2, meal3)
                flight.available_luggage.add(hand_baggage1, hand_baggage2, hand_baggage3)
                flight.available_baggage.add(baggage1, baggage2, baggage3)
                flight.available_services.add(on_board1, on_board2, on_board3)


