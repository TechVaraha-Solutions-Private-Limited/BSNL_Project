from django.urls import path
from . import views
from . import customerviews

urlpatterns = [
   path('', views.index, name='home'),
   path('page/home',views.index),
   path('page/contact',views.contact),
   path('page/project',views.project),
   path('page/gallery',views.gallery),
   path('page/board',views.board),
   path('page/services',views.services, name='services'),
   # path('signin',views.signin,name='signin'),
   path('page/about',views.about),
   # customer views
   path('customer/home',customerviews.home),
   # path('customer/product',customerviews.product,name='product'),
   path('customer/payment',customerviews.payment),
   path('customer/pdf',customerviews.pdf),
   path('customer/logout',customerviews.logout,name='logout')
]