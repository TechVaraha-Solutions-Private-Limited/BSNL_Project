from django.shortcuts import render, redirect
from .models import User, Role, RoleGroup
from commons.user_roles import check_permission, admin_only
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required



def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(request,email=email, password=password)
        if user and user.is_active:
            login(request, user) 
            return redirect(add_role)
    return render(request, 'login.html')

def add_role(request):
    roles = Role.objects.all()
    if request.method == 'POST':
        role = Role()
        role.name = request.POST.get('name','').strip()
        role.save()
    return render(request, 'role/add_roles.html',{'roles':roles})



def add_role_group(request):
    roles = Role.objects.all()
    
    if request.method == 'POST':
        role_group = RoleGroup()
        role_group.module_name = request.POST.get('name','').strip()
        role_group.add =  request.POST.get('add','').strip()
        role_group.view =  request.POST.get('view','').strip()
        role_group.update =  request.POST.get('update','').strip()
        role_group.remove = request.POST.get('delete','').strip()
        role_group.save()
    return render(request, 'role/add_user_group.html',{'roles':roles})


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
        user.password = request.POST.get('password1','').strip()
        user.save()
    return render(request, 'users/add_user.html')

@login_required
def logout_admin_user(request):
    if request.user.is_authenticated:
        if request.user.role == 'Customer':
            logout(request)
            #return redirect(customerpage)
        else:
            logout(request)
            return redirect(admin_login)



