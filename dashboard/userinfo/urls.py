from django.urls import path

from dashboard.members import views
from dashboard.members import *
from .views import admin_login, add_user, logout_admin_user,signin



urlpatterns = [
    path('', admin_login, name='admin_login'),
    path('add-user', add_user, name='add_user'),
    path('signin',signin,name='signin'),
    path('logout',logout_admin_user, name='logout_admin_user'),
]