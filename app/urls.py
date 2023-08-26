from django.urls import path
from . import views
urlpatterns = [
	path('home1',views.home1,name='home1'),
    path('reg',views.reg,name='reg'),
    path('logout',views.logout,name='logout'),
	path('booksum',views.booksum),
	path('bss',views.bss),
	path('newbooking',views.newbooking,name='newbooking'),
	path('generate',views.generate),
	path('newbooking',views.newbooking),
	path('receipt',views.receipt,name='receipt'),
	path('confirmletter',views.confirmletter),
	path('project',views.project,name='project'),
	path('update_data/<int:id>',views.update_data, name='update_data'),
	path('delete_data/<str:id>',views.delete_data, name='delete_data'),
    path('ugdg',views.ugdg,name='ugdg'),
    path('transfer',views.transfer,name='transfer'),
    path('cancel',views.cancel,name='cancel'),
    path('leadowner',views.leadowner,name='leadowner'),
    path('site_visit',views.site_visit,name='site_visit')
]