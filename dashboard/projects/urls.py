from django.urls import path
from dashboard.projects import views
urlpatterns = [
    path('addproject/',views.addproject, name='addproject'),
    path('addplotsize/',views.addplotsize, name='addplotsize'),
    path('addlandinfo/',views.addlandinfo, name='addlandinfo'),
    path('projectlist/',views.projectlist, name='projectlist'),
    path('landrecords/',views.landrecords, name='landrecords'),
    path('updatelandrecords/<id>',views.updatelandrecords,name='updatelandrecords'),
    path('updatinglandrecords/<id>',views.updatinglandrecords,name='updatinglandrecords'),
    path('deletelandrecords/<id>',views.deletelandrecords,name='deletelandrecords'),
    path('updateprojectlist/<id>',views.updateprojectlist,name='updateprojectlist'),
    path('updatingprojectlist/<id>',views.updatingprojectlist,name='updatingprojectlist'),
    path('deleteprojectlist/<id>',views.deleteprojectlist,name='deleteprojectlist')
]
