
from datetime import datetime
from faulthandler import disable
from tkinter import Widget
from turtle import textinput
from django import forms
from .models import customerInfo , checkInData  , studioPackages  , AssignPackage
from django.forms import ModelForm, Textarea , TextInput 
from django.contrib.admin.widgets import AdminDateWidget

class newStudent(forms.ModelForm):
    #customerName = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    class Meta:
        model = customerInfo
        fields = '__all__'
        labels = {
            'customerName' : 'Full Name',
            'leadsChannel' : 'Lead Channel',
            'leadeAge' : 'Age',
        }
        Widget = {
            'customerName' : forms.TextInput(attrs={'class':'form-control'}),
            'leadsChannel' : forms.TextInput(attrs={'class':'form-control'}),
            'leadeage' : forms.TextInput(attrs={'class':'form-control'}),
        }



class newCheckIn(forms.ModelForm):
    class Meta:
        model = checkInData
        fields = '__all__'

        widgets = {
            'studentId': TextInput(attrs={'placeholder': 'ID' , 'len' : '250'}),
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['studentId'].widget.attrs.update({'autofocus': 'autofocus','required': 'required', 
                                                    'placeholder': 'Student Id'})
                                                

class derivePackageform(forms.ModelForm):
    #customerName = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    class Meta:
        model = studioPackages
        fields = '__all__'
        labels = {
            'PakageName' : 'Package Name'
            }
        widgets = {
            'PakageName': TextInput(attrs={'placeholder': 'Package Name' , 'len' : '250' , 'class':'form-control'}),
            } 

class assignPKGform(forms.ModelForm):
    #StudentId = forms.CharField(label=)
    #customerName = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    class Meta:
        model = AssignPackage
        fields = ('StudentId','packageName','startDate','endDate')
        labels = {'StudentId':''
            }
        widgets = {
            'packageName': forms.Select(attrs={'placeholder': 'Package Name' , 'class':'form-control'}),
            'startDate': forms.DateInput(attrs={'class':'form-control'}),
            'endDate': forms.DateInput(attrs={'class':'form-control'}),
            'StudentId':forms.Textarea(attrs={'hidden':'True'})
        }