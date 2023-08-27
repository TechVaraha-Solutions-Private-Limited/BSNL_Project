from django.shortcuts import render

# Create your views here.
def add_new_bookings(request):
    
    return render(request, 'new_bookings/add_new_bookings.html')