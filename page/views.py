from django.shortcuts import render,redirect, HttpResponse
from app.models import Project,Receipt
from app.models import Newbooking,Role
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def signin(request):
    error_message = None
    users = User.objects.all()
    for user in users:
         print(user.username)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('hello')
        user = authenticate(request, username=username, password=password)
        print(user)

        if user:
            auth_login(request, user)
            print(username)
            try:
                role = Role.objects.get(username=user)
                if role.role == 'admin':
                    print(role)
                    return redirect('home1')
                elif role.role == 'customer':
                    return redirect('customer/home')
                # Add more role checks here
                
            except Role.DoesNotExist:
                error_message = "Role not defined for this user"
        else:
            error_message = "Invalid username or password"

    return render(request,'registration/login.html', {'error_message': error_message})

def index(request):
    data = Project.objects.all()
    context={
        "data":data
    }
    return render(request,'page/home.html', {"data": data})

def contact(request):
    return render(request, 'page/contact.html')

def project(request):
    data = Project.objects.all()
    context={
        "data":data
    }
    
    return render(request, 'page/projects.html', {"data": data})

def services(request):
    return render(request, 'page/services.html')

def gallery(request):
    return render(request, 'page/gallery.html')

def board(request):
    return render(request, 'page/board.html')


def about(request):
    return render(request,'page/about.html  ')

def test(request):
    return render(request,'page/customer/home.html')
 
def product(request):
    value = Receipt.objects.all()
    context={
        "value":value
    }
    return render(request,'page/customer/product.html', {"value": value})




