from django import forms
from .models import Project,LandDetails

class BookingFrom(forms.ModelForm):
    fields = ('projectname,')