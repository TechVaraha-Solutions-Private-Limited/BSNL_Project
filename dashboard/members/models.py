from django.db import models
from bsnl import settings
from dashboard.projects.models import LandDetails,Project
from dashboard.userinfo.models import User

class Bookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # project = models.ForeignKey(Project, on_delete=models.CASCADE)
    seniority_id = models.CharField(max_length=20,unique=True,null=True)
    membership_id = models.CharField(max_length=20,unique=True,null=True)
    status = models.SmallIntegerField(default=1, null=True)
    land_details = models.ForeignKey(LandDetails, on_delete=models.CASCADE)
    old_land_details = models.ForeignKey(LandDetails, related_name ='old_land_details',on_delete=models.CASCADE,null=True)
    total_site_value = models.CharField(max_length=120)
    downpayment = models.CharField(max_length=120)
    site_refer = models.CharField(max_length=120)
    am_no = models.CharField(max_length=20,null=False)
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
    payment_data = models.DateField(null=True)
    amount = models.CharField(max_length=20,null=True)
    transaction = models.CharField(max_length=20)
    ddno =models.CharField(max_length=20)
    dateofreceipt = models.CharField(max_length=20)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on =  models.DateTimeField(auto_now=True)

class Ugdg(models.Model):
     seniority_id = models.ForeignKey(Bookings, on_delete=models.CASCADE)


class Receipts(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	seniorityno=models.ForeignKey(Bookings, on_delete=models.CASCADE)
	dimension=models.CharField(max_length=120)
	amount=models.CharField(max_length=120)
	modeofpay=models.CharField(max_length=120)
	chequeno=models.CharField(max_length=120)
	bank=models.CharField(max_length=120)
	branch=models.CharField(max_length=120)
	paydate=models.DateField(max_length=120)
	paystatus=models.CharField(max_length=120)
	dateofreceipt=models.DateField(max_length=120)
     
class Images(models.Model):
    images = models.ImageField(upload_to= settings.PROJECT_UPLOAD_PATH, null=True) 
    place =models.CharField(max_length=120)
    status =  models.SmallIntegerField(default=1, null=True)

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
    id_card_status = models.CharField(max_length=20,null=True)
    fup_category = models.CharField(max_length=20,null=True)
    install_fup_status = models.CharField(max_length=20,null=True)
    install_fup_date = models.CharField(max_length=20,null=True)
    exep_category = models.CharField(max_length=20,null=True)
    excep_reason = models.CharField(max_length=20,null=True)

class Site_visit(models.Model):
    leadowner = models.ForeignKey(Leadowner, on_delete=models.CASCADE)
    so_done_by = models.CharField(max_length=20,null=True)
    sv_don_by = models.CharField(max_length=20,null=True)
    sv_category = models.CharField(max_length=20,null=True)
    source = models.CharField(max_length=20,null=True)
    booked_no = models.CharField(max_length=20,null=True)
    booked_sry_no = models.CharField(max_length=20,null=True)

class Update_blocked(models.Model):
     project=models.CharField(max_length=50,null=True)
     seniority_no=models.CharField(max_length=50,null=True)
     blocked_date=models.CharField(max_length=50,null=True)
     executive=models.CharField(max_length=50,null=True)
     customer_name=models.CharField(max_length=50,null=True)
     is_active = models.BooleanField(default=True)