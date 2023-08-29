from django.db import models
from bsnl import settings
from dashboard.projects.models import LandDetails
from dashboard.userinfo.models import User
class Bookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(LandDetails, on_delete=models.CASCADE)
    seniority_id = models.CharField(max_length=20,unique=True,null=False)
    membership_id = models.CharField(max_length=20,unique=True,null=False)
    status = models.SmallIntegerField(default=1, null=True)
    dimension = models.CharField(max_length=120)
    total_site_value = models.CharField(max_length=120)
    downpayment = models.CharField(max_length=120)
    site_refer = models.CharField(max_length=120)
    # updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on =  models.DateTimeField(auto_now=True)

class PaymentDetails(models.Model):
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE)
    payment_mode = models.CharField(max_length=20,unique=True,null=False)
    bank = models.CharField(max_length=20,unique=True,null=False)
    branch = models.SmallIntegerField(default=1, null=True)
    receipt_no = models.CharField(max_length=20,unique=True,null=False)
    am_no = models.CharField(max_length=20,unique=True,null=True)
    cheque_no = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    payment_data = models.DateField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on =  models.DateTimeField(auto_now=True)

class Receipt(models.Model):
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

