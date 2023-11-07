from django.db import models
from bsnl import settings
from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
       
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
       
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    



class User(AbstractBaseUser):
    role = models.CharField(max_length=10, null=True)
    email = models.EmailField(verbose_name='email', max_length=100, unique=True, null=True) 
    first_name = models.CharField(max_length=50, null=True) 
    last_name = models.CharField(max_length=50, null=True) 
    mobile_no = models.CharField(max_length=50, null=True)
    is_details_added = models.BooleanField(default=False, null=True)
    is_password_set = models.BooleanField(default=False, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_create = models.DateTimeField(auto_now_add=True, null=True)
    date_joined=models.CharField(max_length=50,null=True)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
    login_type = models.CharField(max_length=50,null=True)
    employee_id = models.CharField(max_length=50,null=True)

    def save(self, *args, **kwargs):
        self.s_password = make_password(self.password)
        super(User, self).save(*args, **kwargs)
   

class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, null=False)
    dob = models.DateField(null=True)
    age = models.CharField(max_length=3,null=True)
    alternate_no = models.CharField(max_length=20,null=True)
    address = models.CharField(max_length=300,null=True)
    city =  models.CharField(max_length=300,null=True)
    state =  models.CharField(max_length=300,null=True)
    panno = models.CharField(max_length=20,null=True)
    aadhhaarno = models.CharField(max_length=20,null=True)
    profile = models.ImageField(upload_to= settings.PROFILE_UPLOAD_PATH, null=True)    
    aadhar_proof = models.ImageField(upload_to= settings.AADHAR_UPLOAD_PATH, null=True)  
    pan_proof = models.ImageField(upload_to= settings.PAN_UPLOAD_PATH, null=True)  
    created_by = models.IntegerField(null=True)
    modified_by = models.IntegerField(null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)
    id_card=models.CharField(max_length=30,default='Pending')
    
class UserNominee(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, null=False)
    nominee_name=models.CharField(max_length=100,null=True)
    nominee_age=models.CharField(max_length=10,null=True)
    address = models.CharField(max_length=300,null=True)
    city =  models.CharField(max_length=300,null=True)
    state =  models.CharField(max_length=300,null=True)
    nominee_relationship=models.CharField(max_length=20,null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)


class UserFamilyDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    member_name=models.CharField(max_length=100,null=True)
    member_age=models.CharField(max_length=10,null=True)
    member_relation = models.CharField(max_length=300,null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

class SeniorTeamLead(models.Model):
    user = models.ForeignKey(User,  on_delete=models.DO_NOTHING, null=False)
    project_head = models.ForeignKey(User, related_name="project_head", on_delete=models.DO_NOTHING, null=False)

class TeamLead(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    sr_team = models.ForeignKey(SeniorTeamLead, on_delete=models.DO_NOTHING, null=False)

class Executive(models.Model):
    user = models.ForeignKey(User,  on_delete=models.DO_NOTHING, null=False)
    teamlead = models.ForeignKey(TeamLead, on_delete=models.DO_NOTHING, null=False)


