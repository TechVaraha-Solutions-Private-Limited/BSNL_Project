from django.db import models
from dashboard.userinfo.models import User
from bsnl import settings
# Create your models here.



#Project
class Project(models.Model):
	projectname=models.CharField(max_length=100)
	shortcode = models.CharField(max_length=100)
	# dp_price = models.IntegerField()
	# first_install = models.IntegerField()
	# second_install = models.IntegerField()
	# third_install = models.IntegerField()
	status = models.SmallIntegerField(default=1, null=True)
	images = models.ImageField(upload_to= settings.PROJECT_UPLOAD_PATH, null=True)  
	address = models.CharField(max_length=100)
	updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on =  models.DateTimeField(auto_now=True)
	

class PlotSize(models.Model):
	plotsize = models.CharField(max_length=10,unique=False)
	status = models.SmallIntegerField(default=1, null=True)
	updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on =  models.DateTimeField(auto_now=True)
	
	
class LandDetails(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	plotsize = models.ForeignKey(PlotSize, on_delete=models.CASCADE)
	per_square_feet_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
	total_amount = models.CharField(max_length=40,)
	down_payment = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
	installment_1 = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
	installment_2 = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
	installment_3 = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
	status = models.SmallIntegerField(default=1, null=True)
	updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on =  models.DateTimeField(auto_now=True)
