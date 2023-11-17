from django.shortcuts import render,redirect, HttpResponse
from dashboard.projects.models import LandDetails,Project
from dashboard.members.models import Bookings,G_image
from dashboard.userinfo.models import User
from django.contrib.auth import authenticate,login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from page.models import Contact
# Create your views here.
# def signin(request):
#     error_message = None
#     users = User.objects.filter(role=1)
#     mobile_no = None
#     if request.method == 'POST':
#         mobile_no = request.POST.get('mobile_no')
#         password = request.POST.get('password')
#         user_email = User.objects.get(mobile_no=mobile_no)
#         user = authenticate(request, email=user_email.email, password=password)
#         if user and user_email.is_active and user_email.role == "Customer":
#             auth_login(request, user)
#             return redirect('/')
#     return render(request, 'registration/login.html')

def index(request):
    data = LandDetails.objects.all()
    projects = Project.objects.filter(status=1).all()
    complete = Project.objects.filter(status=0).all()
    # user = UserDetail.objects.filter(user__is_active=1).all()
    count = Bookings.objects.count
    value = Contact.objects.all()
    context={
        "data":data,
        "projects":projects,
        'complete':complete,
        "count":count,
        "value":value
    }
    return render(request,'page/home.html', context)

def contact(request):
    if request.method == 'POST':
        Contact(
            name = request.POST['name'],
            email = request.POST['email'],
            subject = request.POST['subject'],
            messages = request.POST['message']
            ).save()
    return render(request, 'page/contact.html')

def project(request):
    data = LandDetails.objects.all()
    projects = Project.objects.all()
    
    context={
        "data":data,
        "projects":projects
    }
    
    return render(request, 'page/projects.html',context)

def services(request):
    return render(request, 'page/services.html')

def gallery(request):
    img_view = G_image.objects.all()
    return render(request, 'page/gallery.html',{'img_view':img_view})

def board(request):
    return render(request, 'page/board.html')


def about(request):
    return render(request,'page/about.html  ')

def test(request):
    return render(request,'page/customer/home.html')

def product(request):
    # value = Receipt.objects.all()
    # context={
    #     "value":value
    # }, {"value": value}
    return render(request,'page/customer/product.html')

# @login_required
# def logout(request):
#     if request.user.is_authenticated:
#         logout(request)
#         return redirect(signin)
