from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from dashboard.userinfo.models import User,UserDetail,UserFamilyDetails,UserNominee
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

def profile(request):
    user = request.user
    userdetails=UserDetail.objects.filter(user_id=user.id)
    noimee = UserNominee.objects.filter(user_id=user.id)
    print(user.id)
    for userdetail in userdetails:
        print(userdetail.address)
    context={
        'user':user,
        'userdetails':userdetails,
        'noimee':noimee
    }
    return render(request,'page/customer_view/profile.html',context)