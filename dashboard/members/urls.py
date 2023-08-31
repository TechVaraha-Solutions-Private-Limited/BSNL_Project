from django.urls import path
from .views import *

urlpatterns = [
    path('home',home,name='home'),
    path('newbooking', add_new_bookings, name='newbooking'),
    path('booksum',booksum,name='booksum'),
    path('bss',bss,name='bss'),
    path('generate',generate,name='generate'),
    path('ugdg',ugdg,name='ugdg'),
    path('transfer',transfer,name='transfer'),
    path('site_visit',site_visit,name='site_visit'),
    path('lead_owner',lead_owner,name='lead_owner'),
    path('cancel',cancel,name='cancel'),
    path('receipt',receipts,name='receipt'),
    path('btmt',btmt,name='btmt'),
    path('activemember',activemember,name='activemember'),
    path('inactivemember',inactivemember,name='inactivemember'),
    path('confirmletter',confirmletter,name='confirmletter')
]