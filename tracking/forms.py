from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from django.contrib.auth.forms import UserCreationForm
from .models import *

class updatecustomerform(ModelForm): #for updating a customer
   # email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'email here'}))

    class Meta:
        model = Customer
        fields = ['name','email','phone','profile_pic']
