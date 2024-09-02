from django.contrib import admin
from .models import Flight, City, Airports, Seat


admin.site.register(Flight)
admin.site.register(City)
admin.site.register(Airports)
admin.site.register(Seat)

