from django.urls import path
<<<<<<< HEAD
from .views import admin_login, add_role, add_user, add_role_group, logout_admin_user
from dashboard.members import views
=======
from .views import admin_login, add_user, logout_admin_user
>>>>>>> a85b3fb4c6a331535a76ca779e68fb6bbbd22f43


urlpatterns = [
    path('', admin_login, name='admin_login'),
    path('add-user', add_user, name='add_user'),

    path('logout',logout_admin_user, name='logout_admin_user'),
    
]