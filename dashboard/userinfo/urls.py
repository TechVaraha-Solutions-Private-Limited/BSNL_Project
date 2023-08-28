from django.urls import path
from .views import admin_login, add_role, add_user, add_role_group, logout_admin_user
from dashboard.members import views


urlpatterns = [
    path('', admin_login, name='admin_login'),
    path('add-user', add_user, name='add_user'),
    path('add-role',add_role, name='add_role'),
    path('add-role-group',add_role_group, name='add_role_group'),
    path('logout',logout_admin_user, name='logout_admin_user'),
    
]