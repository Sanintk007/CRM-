from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Company, Contact, Report

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'address', 'website']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['company', 'name', 'email', 'phone']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'details']
