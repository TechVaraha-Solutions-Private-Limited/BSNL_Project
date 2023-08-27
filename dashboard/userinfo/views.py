from django.shortcuts import render
from .models import User, Role, RoleGroup
from commons.user_roles import check_permission, admin_only


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
        user.first_name = request.POST.get('username')
        user.save()
    return render(request, 'users/add_user.html')
