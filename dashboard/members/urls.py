from django.urls import path
from .views import *


urlpatterns = [
    #email
    path('send-email/', send_email_view, name='send_email'),

    path('home',home,name='home'),
    path('newbooking', add_new_bookings, name='newbooking'),
    path('get_dimension',get_dimension,name="get_dimension"),
    path('get_project_id',get_project_id,name="get_project_id"),
    path('get_project_value',get_project_value, name="get_project_value"),
    path('booksum',booksum,name='booksum'),
    path('bss',bss,name='bss'),
    path('generate',generate,name='generate'),
    path('ugdg',ugdg,name='ugdg'),
    path('transfer',transfer,name='transfer'),
    path('site_visit',site_visit,name='site_visit'),
    path('lead_owner',lead_owner,name='lead_owner'),
    path('cancel',cancel,name='cancel'),
    path('receipt',receipts,name='receipt'),
    path('btmt',btmt,name='btmt'),
    path('activemember',activemember,name='activemember'),
    path('inactivemember',inactivemember,name='inactivemember'),
    path('confirmletter',confirmletter,name='confirmletter'),
    path('view_history',view_history,name='view_history'),
    path('print_receipt',print_receipt,name='print_receipt'),
    path('user_access',user_access,name='user_access'),
    path('view_user_access',view_user_access,name='view_user_access'),
    path('rate_update',rate_update,name='rate_update'),
    path('view_rate_update',view_rate_update,name='view_rate_update'),
    path('update_sales_staff',update_sales_staff,name='update_sales_staff'),
    path('view_update_sales_staff',view_update_sales_staff,name='view_update_sales_staff'),
    path('blocked_seniority',blocked_seniority,name='blocked_seniority'),
    path('view_blocked_seniority',view_blocked_seniority,name='view_blocked_seniority'),
    path('view_update_pdc',view_update_pdc,name='view_update_pdc'),
    path('cr_code',cr_code,name='cr_code'),
    path('view_site_visit',view_site_visit,name='view_site_visit'),
    path('view_receipt/<id>',view_receipt,name='view_receipt'),
    path('view_call_request',view_call_request,name='view_call_request'),
    
    # update function
    path('updateactivememberlist/<id>',updateactivememberlist,name='updateactivememberlist'),
    path('update_personal/<id>',update_personal,name='update_personal'),
    path('update_site_visit/<id>',update_site_visit,name='update_site_visit'),
    path('update_inactive/<id>',update_inactive,name='update_inactive'),
    path('update_pdc',update_pdc,name='update_pdc'),
    path('update_block/<id>',update_block,name='update_block'),
    path('update_receipts/<id>',update_receipts,name='update_receipts'),
    # delete function
    path('deleteactivememberlist/<id>',deleteactivememberlist,name='deleteactivememberlist'),
    path('delete_site_visit/<id>',delete_site_visit,name='delete_site_visit'),
    path('delete_block/<id>',delete_block,name='delete_block'),
    path('delete_user_access/<id>',delete_user_access,name='delete_user_access'),
    # images
    path('banner_images',banner_images,name='banner_images'),
    path('gallery_images',gallery_images,name='gallery_images'),
    path('deletingimage/<id>',deletingimage,name='deletingimage'),
    #add Customer
    path('addcustomer',addcustomer,name='addcustomer'),
    path('user_access/<id>',user_access,name='user_access'),
    path('get-team-owner',get_team_owner,name="get_team_owner"),
    #add new customer using site Visit
    path('site_visit/<id>',site_visit_custmer,name='site_visit_custmer'),
    #View Member
    path('view_member',view_member,name='view_member'),
]