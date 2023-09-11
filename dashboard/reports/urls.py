from django.urls import path
from dashboard.reports import views


urlpatterns=[
    path('confirmletter_view',views.confirmletter_view,name='confirmletter_view'),
]