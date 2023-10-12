from django.shortcuts import render,redirect
from dashboard.members.models import Bookings,PaymentDetails
from dashboard.userinfo.models import UserDetail
# Create your views here.
def confirmletter_view(request,id):
    user=Bookings.objects.get(id=id)
    userdetail = UserDetail.objects.get(user=user.user)
    payment = PaymentDetails.objects.get(booking_id=user.id)
    print(payment.am_no)
    return render(request,'confirmletter_view.html',{'user':user,'userdetail':userdetail,'payment':payment})