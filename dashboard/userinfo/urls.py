from django.urls import path
from .views import add_role, add_user, add_role_group


urlpatterns = [
    path('', add_user, name='add_user'),
    path('add-role',add_role, name='add_role'),
    path('add-role-group',add_role_group, name='add_role_group'),
]