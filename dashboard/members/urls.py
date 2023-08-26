from django.urls import path
from ..userdata.views import add_new_bookings


urlpatterns = [
    path('', add_new_bookings, name='add_new_bookings'),
]