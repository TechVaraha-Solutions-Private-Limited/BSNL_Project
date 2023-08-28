from django.urls import path
from .views import add_new_bookings,booksum,bss


urlpatterns = [
    path('newbooking', add_new_bookings, name='newbooking'),
    path('booksum',booksum,name='booksum'),
    path('bss',bss,name='bss'),
]