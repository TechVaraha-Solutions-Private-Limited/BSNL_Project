from django.urls import path
from dashboard.reports import views


urlpatterns=[
    path('confirmletter_view/<id>',views.confirmletter_view,name='confirmletter_view'),
    path('print_recepit/<id>',views.print_recepit,name='print_recepit'),
]