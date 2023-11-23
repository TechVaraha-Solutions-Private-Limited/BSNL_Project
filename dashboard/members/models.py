from django.db import models
from bsnl import settings
from dashboard.projects.models import LandDetails,Project
from dashboard.userinfo.models import User
from dashboard.userinfo.models import UserDetail

class Site_visit(models.Model):
    date_of_site_visit = models.DateTimeField(max_length=20,null=True)
    cust_name = models.CharField(max_length=20,null=True)
    phone_no = models.CharField(max_length=20,null=True)
    executive = models.ForeignKey(User, on_delete=models.CASCADE)
    team_lead = models.ForeignKey(User,related_name='team_lead', on_delete=models.CASCADE)
    proj_head = models.ForeignKey(User, related_name='proj_head',on_delete=models.CASCADE)
    so_done_by = models.CharField(max_length=20,null=True)
    sv_don_by = models.CharField(max_length=20,null=True)
    sv_category = models.CharField(max_length=20,null=True)
    source = models.CharField(max_length=20,null=True)
    booked_no = models.DateTimeField(max_length=20,null=True)
    booked_sry_no = models.CharField(max_length=20,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on =  models.DateTimeField(auto_now=True)
    status =  models.BooleanField(default=True)
    sv_status = models.CharField(max_length=20,null=True)

class Bookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seniority_id = models.CharField(max_length=20,unique=True,null=True)
    membership_id = models.CharField(max_length=20,unique=True,null=True)
    status = models.SmallIntegerField(default=1, null=True)
    land_details = models.ForeignKey(LandDetails, on_delete=models.CASCADE)
    old_land_details = models.ForeignKey(LandDetails, related_name ='old_land_details',on_delete=models.CASCADE,null=True)
    total_site_value = models.CharField(max_length=120)
    downpayment = models.CharField(max_length=120)
    site_refer = models.CharField(max_length=120)
    am_no = models.CharField(max_length=20,null=False)
    payments_status = models.CharField(max_length=2,default=0)
    total_paid_amount = models.CharField(max_length=100,default=0)
    #UGDG
    date_of_change = models.CharField(max_length=120,null=True)
    type_of_change = models.CharField(max_length=120,null=True)
    diff = models.CharField(max_length=20,null=True)
    exective = models.CharField(max_length=20,null=True)
    team_lead = models.CharField(max_length=20,null=True) 
    sr_team_lead = models.CharField(max_length=20,null=True)
    project_lead = models.CharField(max_length=20,null=True)
    type_bkg = models.CharField(max_length=20,null=True)
    indvl_paid = models.CharField(max_length=20,null=True)
    tl_paid = models.CharField(max_length=20,null=True)
    stl_paid = models.CharField(max_length=20,null=True)
    #Tranfer
    date_of_transfer = models.CharField(max_length=20,null=True)
    type_of_transfer = models.CharField(max_length=30,null=True)
    transfer_to = models.ForeignKey(User,related_name ='transfer_to', on_delete=models.CASCADE,null=True)
    old_seniority_id =models.CharField(max_length=20,unique=True,null=True)
    affidavit = models.ImageField(upload_to= settings.PROJECT_UPLOAD_PATH, null=True)
    death_cert =models.ImageField(upload_to= settings.PROJECT_UPLOAD_PATH, null=True)
    #cancel
    date_of_cancel = models.CharField(max_length=20,null=True)
    type_of_cancel = models.CharField(max_length=20,null=True)
    date_of_refund = models.CharField(max_length=20,null=True)
    mode_of_refund = models.CharField(max_length=20,null=True)
    refund_cheque_no = models.CharField(max_length=20,null=True)
    refund_amount = models.CharField(max_length=20,null=True)
    type_of_refund = models.CharField(max_length=20,null=True)
    issued_by = models.CharField(max_length=20,null=True) 
    sitevist = models.ForeignKey(Site_visit, on_delete=models.CASCADE,null=True)
    # updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on =  models.DateTimeField(auto_now=True)

class PaymentDetails(models.Model):
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE,null=True)
    payment_mode = models.CharField(max_length=20,null=True)
    bank = models.CharField(max_length=20,null=True)
    branch = models.CharField(max_length=200,null=True)
    receipt_no = models.CharField(max_length=20,null=False)
    cheque_no = models.CharField(max_length=20,null=True)
    payment_data = models.CharField(max_length=50,null=True)
    amount = models.CharField(max_length=20,null=True)
    transaction = models.CharField(max_length=20)
    ddno =models.CharField(max_length=20)
    dateofreceipt = models.CharField(max_length=20)
    paymentname = models.CharField(max_length=20,null=True)
    status = models.CharField(max_length=2,default=0)
    total_paid_amount = models.CharField(max_length=100,default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on =  models.DateTimeField(auto_now=True)
    date_cleared=models.DateField(null=True)
    fup_date=models.DateField(null=True)

class Ugdg(models.Model):
     seniority_id = models.ForeignKey(Bookings, on_delete=models.CASCADE)
    
class Images(models.Model):
    images = models.ImageField(upload_to= settings.PROJECT_UPLOAD_PATH, null=True) 
    place =models.CharField(max_length=120)
    status =  models.SmallIntegerField(default=1, null=True)

class G_image(models.Model):
    gallery_image= models.ImageField(upload_to= settings.PROFILE_UPLOAD_PATH,null=True)
    g_place= models.CharField(max_length=150)
    g_status= models.SmallIntegerField(default=1, null=True)

class Leadowner(models.Model):
    seniorityno_id = models.CharField(max_length=20,null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    executive = models.CharField(max_length=20,null=True)
    team_lead = models.CharField(max_length=20,null=True)
    sr_team_lead =models.CharField(max_length=20,null=True)
    project_head = models.CharField(max_length=20,null=True)
    type_of_booking = models.CharField(max_length=20,null=True)
    ref_exis_cust_sry = models.CharField(max_length=20,null=True)
    ref_exis_cust_name = models.CharField(max_length=20,null=True)
    date_of_sitevisit = models.CharField(max_length=20,null=True) 
    sv_done_cust = models.CharField(max_length=20,null=True)
    source = models.CharField(max_length=20,null=True)
    fup_category = models.CharField(max_length=20,null=True)
    install_fup_status = models.CharField(max_length=20,null=True)
    install_fup_date = models.CharField(max_length=20,null=True)
    exep_category = models.CharField(max_length=20,null=True)
    excep_reason = models.CharField(max_length=20,null=True)


class Update_blocked(models.Model):
     project=models.CharField(max_length=50,null=True)
     seniority_no=models.CharField(max_length=50,null=True)
     blocked_date=models.CharField(max_length=50,null=True)
     executive=models.CharField(max_length=50,null=True)
     customer_name=models.CharField(max_length=50,null=True)
     is_active = models.BooleanField(default=True)

class Btmt(models.Model):
    date_of_credit = models.CharField(max_length=50,null=True)
    transaction_particulars = models.CharField(max_length=50,null=True)
    cheque_no = models.CharField(max_length=50,null=True)
    statemnt_amount = models.CharField(max_length=50,null=True)
    trans_category = models.CharField(max_length=50,null=True)
    trans_amount = models.CharField(max_length=50,null=True)
    receipt_no = models.CharField(max_length=50,null=True)
    cr_dr_Code = models.CharField(max_length=50,null=True)
    code_description = models.CharField(max_length=50,null=True)
    seniority_no = models.CharField(max_length=50,null=True)
    amt_remark = models.CharField(max_length=50,null=True)
    project = models.CharField(max_length=40,null=True)
    
class Request_call(models.Model):
    cust_name = models.CharField(max_length=50,null=True)
    cust_number = models.IntegerField(null=True)
    time_of_request = models.DateTimeField(auto_now=True)