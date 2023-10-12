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
    total_site_value = models.CharField(max_length=120)
    downpayment = models.CharField(max_length=120)
    site_refer = models.CharField(max_length=120)
    # updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on =  models.DateTimeField(auto_now=True)

class PaymentDetails(models.Model):
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE,null=True)
    payment_mode = models.CharField(max_length=20,null=True)
    bank = models.CharField(max_length=20,null=True)
    branch = models.CharField(max_length=200,null=True)
    receipt_no = models.CharField(max_length=20,null=False)
    am_no = models.CharField(max_length=20,null=False)
    cheque_no = models.CharField(max_length=20,null=True)
    payment_data = models.DateField(null=True)
    amount = models.CharField(max_length=20,null=True)
    transaction = models.CharField(max_length=20)
    ddno =models.CharField(max_length=20)
    payment_mode = models.CharField(max_length=20,null=True)
    dateofreceipt = models.CharField(max_length=20)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on =  models.DateTimeField(auto_now=True)



class Ugdg(models.Model):
     seniority_id = models.ForeignKey(Bookings, on_delete=models.CASCADE)
     cut_name = models.CharField(max_length=50)
     date_of_change = models.DateField()
     type_of_change = models.CharField(max_length=120)
     sft_form = models.CharField(max_length=20)
     sft_to = models.CharField(max_length=20)
     diff = models.CharField(max_length=20)
     exective = models.CharField(max_length=20)
     team_lead = models.CharField(max_length=20)
     sr_team_lead = models.CharField(max_length=20)
     project_lead = models.CharField(max_length=20)
     type_bkg = models.CharField(max_length=20)
     indvl_paid = models.CharField(max_length=20,null=True)
     tl_paid = models.CharField(max_length=20,null=True)
     stl_paid = models.CharField(max_length=20,null=True)




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