from django.db import models
from dashboard.userinfo.models import User
from bsnl import settings
# Create your models here.



#Project
class Project(models.Model):
	projectname=models.CharField(max_length=100, null=True)
	shotcode = models.CharField(max_length=100)
	dp_price = models.CharField(max_length=100)
	first_install = models.CharField(max_length=100)
	second_install = models.CharField(max_length=100)
	third_install = models.CharField(max_length=100)
	status = models.CharField(max_length=100)
	images = models.ImageField(upload_to= settings.PROJECT_UPLOAD_PATH, null=True)  
	address = models.CharField(max_length=100)
	updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on =  models.DateTimeField(auto_now=True)
	

class PlotSize(models.Model):
	plotsize = models.CharField(max_length=10,unique=True)
	status = models.SmallIntegerField(default=1, null=True)
	updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on =  models.DateTimeField(auto_now=True)
	
	
class LandDetails(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	plotsize = models.ForeignKey(PlotSize, on_delete=models.CASCADE)
	per_square_feet_amount = models.DecimalField(max_digits=10, decimal_places=2)
	total_amount = models.DecimalField(max_digits=10, decimal_places=2)
	down_payment = models.DecimalField(max_digits=10, decimal_places=2)
	installment_1 = models.DecimalField(max_digits=10, decimal_places=2)
	installment_2 = models.DecimalField(max_digits=10, decimal_places=2)
	installment_3 = models.DecimalField(max_digits=10, decimal_places=2)
	status = models.SmallIntegerField(default=1, null=True)
	updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on =  models.DateTimeField(auto_now=True)



