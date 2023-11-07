from django.urls import path
from dashboard.reports import views


urlpatterns=[
    path('confirmletter_view/<id>',views.confirmletter_view,name='confirmletter_view'),
    path('print_recepit/<id>',views.print_recepit,name='print_recepit'),
    path('bookingreport',views.booking_report,name='booking_report'),
    path('sitereport',views.site_report,name='site_report'),
    path('pdcreport',views.pdc_report,name='pdc_report'),
    path('ugdgreport',views.ugdg_report,name='ugdg_report'),
    path('transferreport',views.transfer_report,name='transfer_report'),
    path('cancelreport',views.cancel_report,name='cancel_report'),
    path('receiptdetails',views.receipt_details,name='receipt_details'),
]