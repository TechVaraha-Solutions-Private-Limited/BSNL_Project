from django.shortcuts import render, redirect
# from commons.user_roles import check_permission, admin_only
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from .models import User,SeniorTeamLead,TeamLead,Executive
from django.contrib.auth.hashers import make_password
from django.contrib import messages


def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('/members/home')
            else:
               
                messages.error(request, 'Your account is not active.')
        else:
           
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'login.html')

# @admin_only
# @check_permission('user', 'add')
def add_user(request):
    sr_team = User.objects.filter(role='Project_Lead')
    team = SeniorTeamLead.objects.all()
    execut = TeamLead.objects.all()
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        role = request.POST.get('role')
        mobile_no = request.POST.get('mobile_no', '').strip()
        email = request.POST.get('email', '').strip()
        password = make_password(request.POST.get('password1', '').strip())
        employee_id = request.POST.get('employee_id', '').strip()
        date_joined = request.POST.get('date_joined', '').strip()
        if not first_name:
            messages.error(request, 'Email already exists.')
            return render(request, 'users/add_user.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'users/add_user.html', {'sr_team_lead': sr_team, 'team': team, 'executive': execut})
        
        if User.objects.filter(mobile_no=mobile_no).exists():
            messages.error(request, 'Mobile number already exists.')
            return render(request, 'users/add_user.html', {'sr_team_lead': sr_team, 'team': team, 'executive': execut})

        user = User(
            first_name=first_name,
            last_name=last_name,
            role=role,
            mobile_no=mobile_no,
            email=email,
            password=password,
            employee_id=employee_id,
            date_joined=date_joined
        )
        user.save()

        value = request.POST.get('role')
        if value == 'Sr_Team_lead':
            sr_team_lead = SeniorTeamLead()
            sr_team_lead.user = user
            sr_team_lead.project_head_id = request.POST.get('project_lead')
            sr_team_lead.save()
        elif value == 'Team_Lead':
            team_lead = TeamLead()
            team_lead.user = user
            team_lead.sr_team_id = request.POST.get('sr_team_lead')
            team_lead.save()
        elif value == 'Executive':
            executive = Executive()
            executive.user = user
            executive.teamlead_id = request.POST.get('team_lead')
            executive.save()

    context = {
        'sr_team_lead': sr_team,
        'team': team,
        'executive': execut
    }
    messages.error(request,'Successfully Saved')
    return render(request, 'users/add_user.html', context)
def signin(request):
    if request.method == 'POST':
        mobile_no = request.POST.get('mobile_no')
        password = request.POST.get('password')
        
        try:
            user_email = User.objects.get(mobile_no=mobile_no)
        except User.DoesNotExist:
            messages.error(request, "Invalid credentials")
            return render(request, 'registration/login.html')
        
        user = authenticate(request, username=user_email.username, password=password)
        
        if user is not None:
            if user_email.is_active and user_email.role == "Customer":
                auth_login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Your account is not active or unauthorized.")
        else:
            messages.error(request, "Invalid credentials")
    
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