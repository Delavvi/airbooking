from django.urls import path
from .views import FlightsList, search_origin, search_departure, DetailFlight, SeatListView, FlightServicesView
from .api_view import SeatsDetailView, AirplaneDetailView

app_name = "client_interface"

urlpatterns = [
    path('', FlightsList.as_view(), name='flight_list'),
    path('search-origin', search_origin, name='origin_list'),
    path('search-departure', search_departure, name='departure_list'),
    path('flights/<int:pk>', DetailFlight.as_view(), name='flight'),
    path('plane_template/<int:pk>', SeatListView.as_view(), name='plane'),
    path('seats', SeatsDetailView.as_view(), name='seats'),
    path('airplane', AirplaneDetailView.as_view(), name='airplane'),
    path('get_services/<int:pk>', FlightServicesView.as_view(), name='services')
]
