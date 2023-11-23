from django.db import models
from dashboard.userinfo.models import User
from bsnl import settings
# Create your models here.



#Project
class Project(models.Model):
	projectname=models.CharField(max_length=100)
	shortcode = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	pincode = models.IntegerField()
	status = models.SmallIntegerField(default=1, null=True)
	images = models.ImageField(upload_to= settings.PROJECT_UPLOAD_PATH, null=True)  
	address = models.CharField(max_length=100)
	updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on =  models.DateTimeField(auto_now=True)
	gmap = models.CharField(max_length=1000,null=True)
	pdf_file = models.FileField(upload_to= settings.PDF_UPLOAD_PATH,null=True)

class PlotSize(models.Model):
	plotsize = models.CharField(max_length=10,unique=False)
	status = models.SmallIntegerField(default=1, null=True)
	updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on =  models.DateTimeField(auto_now=True)
	
	
class LandDetails(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	plotsize = models.ForeignKey(PlotSize, on_delete=models.CASCADE)
	per_square_feet_amount = models.CharField(max_length=40)
	total_amount = models.CharField(max_length=40)
	down_payment = models.CharField(max_length=40)
	installment_1 = models.CharField(max_length=40)
	installment_2 = models.CharField(max_length=40)
	installment_3 = models.CharField(max_length=40)
	status = models.SmallIntegerField(default=1, null=True)
	updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on =  models.DateTimeField(auto_now=True)
