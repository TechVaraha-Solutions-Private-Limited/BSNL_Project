from django.shortcuts import render, redirect
# from commons.user_roles import check_permission, admin_only
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib.auth.hashers import make_password

def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(request,email=email, password=password)
        if user and user.is_active:
            auth_login(request, user)
            return redirect('/members/home')
    return render(request, 'login.html')

# @admin_only
# @check_permission('user', 'add')
def add_user(request):
    if request.method == 'POST':
        user = User()
        user.first_name = request.POST.get('first_name','').strip()
        user.last_name = request.POST.get('last_name','').strip()
        user.role = request.POST.get('role')
        user.mobile_no = request.POST.get('mobile_no','').strip()
        user.email = request.POST.get('email','').strip()
        user.password = make_password(request.POST.get('password1','').strip())
        user.save()
    return render(request, 'users/add_user.html')
def signin(request):
    if request.method == 'POST':
        mobile_no = request.POST.get('mobile_no')
        password = request.POST.get('password')
        user_email = User.objects.get(mobile_no=mobile_no)
        user = authenticate(request, email=user_email.email, password=password)
        if user and user_email.is_active and user_email.role == "Customer":
            auth_login(request, user)
            return redirect('/')
    return render(request, 'registration/login.html')

@login_required
def logout_admin_user(request):
    if request.user.is_authenticated:
        if request.user.role == 'Customer':
            logout(request)
            return redirect(signin)
        else:
            logout(request)
            return redirect(admin_login)



