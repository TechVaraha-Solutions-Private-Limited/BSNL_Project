from django.db import models
from dashboard.members.models import User
from bsnl import settings
# Create your models here.


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

	
class LandInformation(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	plotsize = models.ForeignKey(PlotSize, on_delete=models.CASCADE)
	status = models.SmallIntegerField(default=1, null=True)
	updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on =  models.DateTimeField(auto_now=True)