from django import forms
from django.forms import ModelForm
from .models import Newbooking,Project,Receipt,Role
CHOOSE_CHOICES = (
	('customer','CUSTOMER'),
	('admin','ADMIN'),
	('adminuser','ADMINUSER'),
	
)
class NewbookingForm(forms.Form):
	username = forms.CharField(max_length=120)
	fathername = forms.CharField(max_length=120)
	dob = forms.DateField()
	age = forms.CharField(max_length=100)
	moblieno = forms.CharField(max_length=100)
	alternateno = forms.CharField(max_length=100)
	emailid = forms.CharField(max_length=100)
	address = forms.CharField(max_length=100)
	panno = forms.CharField(max_length=100)
	aadhhaarno = forms.CharField(max_length=100)
	nomieename = forms.CharField(max_length=100)
	nomieeage = forms.CharField(max_length=100)
	nomieerelationship = forms.CharField(max_length=100)
	nomieeaddress = forms.CharField(max_length=100)
	project = forms.CharField(max_length=100)
	dimension = forms.CharField(max_length=100)
	total= forms.CharField(max_length=100)
	downpayment = forms.CharField(max_length=100)
	siterefer = forms.CharField(max_length=100)
	modeofpay = forms.CharField(max_length=100)
	bank = forms.CharField(max_length=100)
	branch = forms.CharField(max_length=100)
	chequeno = forms.CharField(max_length=100)
	paydate = forms.DateField()
	amount = forms.CharField(max_length=100)
	seniorityno = forms.CharField(max_length=100)
	amno = forms.CharField(max_length=100)
	receiptno = forms.CharField(max_length=100)
	familymemname=forms.CharField(max_length=100)
	familymemage=forms.CharField(max_length=10)
	familymemrelation=forms.CharField(max_length=100)
	role=forms.ChoiceField(choices = CHOOSE_CHOICES)
	password=forms.CharField(max_length=100)
class ProjectForm(forms.ModelForm):
	class Meta:
		model=Project
		fields='__all__'
class ReceiptForm(forms.ModelForm):
	class Meta:
		model=Receipt
		fields = ['username', 'seniorityno', 'dimension', 'amount', 'modeofpay', 'chequeno', 'bank', 'branch', 'paydate', 'paystatus', 'dateofreceipt']
class SearchForm(forms.Form):
	seniorityno = forms.CharField(max_length=120)
class AdminuserForm(forms.Form):
	username=forms.CharField(max_length=120)
	fathername=forms.CharField(max_length=120)
	dob=forms.DateField()
	age=forms.CharField(max_length=120)
	moblieno=forms.CharField(max_length=120)
	address=forms.CharField(max_length=120)
	alternateno=forms.CharField(max_length=120)
	panno=forms.CharField(max_length=120)
	aadhhaarno=forms.CharField(max_length=120)
	poision=forms.CharField(max_length=120)
	role=forms.ChoiceField(choices = CHOOSE_CHOICES)
	emailid=forms.CharField(max_length=120)
	password=forms.CharField(max_length=100)