from django.shortcuts import render
from django.db.models import Min
from django.views.generic import ListView, DetailView, TemplateView
from authentication.models import Flight, City, Seat, AirplaneType, AdditionalServices
from django.db.models import Count, Q
from datetime import datetime, timedelta
import pytz
from django.utils.timezone import localtime
import json
from .forms import PassengerForm
from .serializer import SeatSerializer


def get_lowest_price(flight: Flight, flight_class: str) -> float:
    price = flight.available_meal.aggregate(Min('price'))['price__min'] + flight.available_baggage.aggregate(Min('price'))['price__min']
    if flight_class == 'FC':
        price += flight.first_seat_price
    elif flight_class == 'BC':
        price += flight.business_seat_price
    else:
        price += flight.economy_seat_price
    return price


class FlightsList(ListView):
    model = Flight
    template_name = 'home.html'
    paginate_by = 10

    def get_queryset(self):
        origin = self.request.GET.get('origin')
        destination = self.request.GET.get('departure')
        time = self.request.GET.get('date_of_flight')
        passengers = self.request.GET.get('passengers')
        seat_class = self.request.GET.get('class')
        if origin and destination and time and passengers:
            date_of_flight = datetime.strptime(time, '%Y-%m-%d').replace(tzinfo=pytz.UTC)
            end_date = date_of_flight + timedelta(days=1)
            destination_cities = City.objects.filter(name__icontains=destination)
            origin_cities = City.objects.filter(name__icontains=origin)
            queryset = Flight.objects.annotate(
                num_seats=Count('seats', filter=Q(seats__flight_class=seat_class))
            ).filter(
                destination__in=destination_cities,
                origin__in=origin_cities,
                num_seats__gte=passengers,
                date_of_flight__range=[date_of_flight, end_date]
            ).order_by('date_of_flight').select_related(
                'arrival_airport', 'departure_airport', 'destination', 'origin'
            )
            return queryset
        queryset = super().get_queryset()
        return queryset.order_by('date_of_flight')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flight_class = self.request.GET.get('class')
        for flight in context['page_obj']:
            flight.seat_price = get_lowest_price(flight, flight_class)
            flight.duration = flight.arriving_date - flight.date_of_flight
        return context


def search_origin(request):
    search_text = request.POST.get('origin')
    results = City.objects.filter(name__icontains=search_text)
    context = {'origin_results': results}
    return render(request, 'search_results.html', context=context)


def search_departure(request):
    search_text = request.POST.get('departure')
    results = City.objects.filter(name__icontains=search_text)
    context = {'departure_results': results}
    return render(request, 'search_results.html', context=context)


class DetailFlight(DetailView):
    model = Flight
    template_name = 'modal/flight_info.html'

    def get_queryset(self):
        return super().get_queryset().select_related('airplane')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flight = self.object
        start_time = localtime(flight.date_of_flight)
        end_time = localtime(flight.arriving_date)
        duration = end_time - start_time
        context['flight_duration'] = duration
        context['base'] = get_lowest_price(flight, 'EC')
        context['first'] = get_lowest_price(flight, 'FC')
        context['business'] = get_lowest_price(flight, 'BC')
        return context


class SeatListView(ListView):
    model = Seat
    template_name = 'booking_seats/airplane.html'

    def get_queryset(self):
        flight_id = self.kwargs.get('pk')
        seats = Seat.objects.filter(flight_id=flight_id).order_by('pk')
        return seats if seats else None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        flight_id = self.kwargs.get('pk')
        flight = Flight.objects.select_related('airplane').get(pk=flight_id)
        plane_type: AirplaneType = flight.airplane.type
        business_index = plane_type.business_seats
        first_class_index = business_index + plane_type.premium_seats
        seats = context['object_list']
        context['business_seats'] = seats[:business_index]
        context['first_class_seats'] = seats[business_index:first_class_index]
        context['economy_seats'] = seats[first_class_index:]
        context['flight_id'] = flight_id
        context['seats_per_business_row'] = plane_type.seats_per_business_row
        context['seats_per_first_class_row'] = plane_type.seats_per_first_class_row
        context['seats_per_economy_row'] = plane_type.seats_per_economy_row

        seat_data = {
            'business_seats': SeatSerializer(seats[:business_index], many=True).data,
            'first_class_seats': SeatSerializer(seats[business_index:first_class_index], many=True).data,
            'economy_seats': SeatSerializer(seats[first_class_index:], many=True).data,
            'seats_per_business_row': plane_type.seats_per_business_row,
            'seats_per_first_class_row': plane_type.seats_per_first_class_row,
            'seats_per_economy_row': plane_type.seats_per_economy_row
        }
        context['seat_data_json'] = json.dumps(seat_data)
        return context


class FlightServicesView(DetailView):
    model = AdditionalServices
    template_name = 'booking_seats'

    def get_queryset(self):
        return super().get_queryset().fetch_related('available_meal', 'available_luggage'
                                                                    ,'available_baggage', 'available_services')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        seats = self.request.get('seats')
        seats = Seat.objects.filter(pk__in=seats)
        context['seats'] = seats
        form = PassengerForm()
        context['form'] = form
        return context


