from rest_framework import viewsets
from authentication.models import Seat, Flight
from .serializer import SeatSerializer, AirplaneTypeSerializer
from rest_framework import generics


class SeatsDetailView(generics.RetrieveAPIView):
    serializer_class = SeatSerializer

    def get_queryset(self):
        flight_id = self.request.query_params.get('flight_id')
        seats = Seat.objects.get(flight_id=flight_id).order_by('number')
        return seats if seats else None


class AirplaneDetailView(generics.RetrieveAPIView):
    serializer_class = AirplaneTypeSerializer

    def get_queryset(self):
        flight_id = self.request.query_params.get('flight_id')
        flight = Flight.objects.filter(flight_id=flight_id)
        return flight.airplane.type
