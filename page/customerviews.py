from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from dashboard.userinfo.models import User,UserDetail,UserFamilyDetails,UserNominee
from dashboard.members.models import Bookings,PaymentDetails
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
# from app.models import Newbooking
from django.http import FileResponse
from django.views.generic import View
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
@login_required
def profile(request):
    user = request.user
    userdetails=UserDetail.objects.filter(user_id=user.id)
    noimee = UserNominee.objects.filter(user_id=user.id)
    family = UserFamilyDetails.objects.filter(user_id=user.id)
    context={
        'user':user,
        'userdetails':userdetails,
        'noimee':noimee,
        'family':family
    }
    return render(request,'page/customer_view/profile.html',context)
@login_required
def booking(request):
    user = request.user
    landdetails=Bookings.objects.filter(mobile_no=user.mobile_no)
    for payment in landdetails:
        paymentView= PaymentDetails.objects.filter(booking_id = payment.id)
        for pay in paymentView:
            payment.status = pay.paymentname
            payment.totalamout = pay.amount
        print(payment.totalamout)
    context = {
        'landdetails':landdetails
    }
    return render(request,'page/customer_view/booking.html',context)