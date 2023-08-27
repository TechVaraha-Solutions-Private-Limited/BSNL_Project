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
    # updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on =  models.DateTimeField(auto_now=True)

class PaymentDetails(models.Model):
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE)
    payment_mode = models.CharField(max_length=20,unique=True,null=False)
    bank = models.CharField(max_length=20,unique=True,null=False)
    branch = models.SmallIntegerField(default=1, null=True)
    cheque_no = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    payment_data = models.DateField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on =  models.DateTimeField(auto_now=True)
