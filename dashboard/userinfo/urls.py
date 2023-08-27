from django.urls import path
from .views import admin_login, add_user, logout_admin_user


urlpatterns = [
    path('', admin_login, name='admin_login'),
    path('add-user', add_user, name='add_user'),

    path('logout',logout_admin_user, name='logout_admin_user'),
]