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
   path('page/privacy',views.privacy),
   path('page/services',views.services, name='services'),
   # path('signin',views.signin,name='signin'),
   path('page/about',views.about),
   # path('logout',views.logout),
   # customer views
   path('profile',customerviews.profile,name='profile'),
   path('booking',customerviews.booking,name='booking'),
]