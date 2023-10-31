from django.shortcuts import render,redirect
from dashboard.members.models import Bookings,PaymentDetails
from dashboard.projects.models import Project
from dashboard.userinfo.models import UserDetail
# Create your views here.
def confirmletter_view(request,id):
    book=Bookings.objects.get(id=id)
    userdetail = UserDetail.objects.get(user=book.user)
    payment = PaymentDetails.objects.filter(booking=book)
    return render(request,'confirmletter_view.html',{'user':book,'userdetail':userdetail,'payment':payment})

def print_recepit(request,id):
    user=Bookings.objects.get(id=id)
    userdetail = UserDetail.objects.get(user=user.user)

    payments = PaymentDetails.objects.filter(booking_id=user.id)
    for payment in payments:
        print(payment.id)
    return render (request,'print_recepit.html',{'user':user,'userdetail':userdetail,'payment':payments})

def booking_report(request):
    view_report = Bookings.objects.all()
    return render(request, 'booking_report.html', {'view_report': view_report})