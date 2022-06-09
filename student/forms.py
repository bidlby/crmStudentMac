

from django import forms
from .models import checkInByUserModel, customerInfo , checkInData  , studioPackages  , AssignPackage , customersPayments , FollowUpModel
from django.forms import ChoiceField, ModelForm, Textarea , TextInput 
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin import widgets
from django.forms.fields import DateField



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
            'courseName' : 'Course Name',
            'group_age' : 'Group Age',
            'numberOfLessons' : 'Total Lessons',
            'packagePrice' : 'Package Price',
            'PakageName' : 'Package Name',
            }

        widgets = {
              'PakageName': TextInput(attrs={
              'placeholder': 'Package Name' ,
              'len' : '250' ,
              'class':'form-control'
              }),
              'group_age' : forms.Select(attrs={
                  'placeholder':'group Age',
                  'class':'form-control',
                  'style': 'width:16ch',
              }),
                  'courseName' : forms.Select(attrs={
                  'placeholder':'Course Name',
                  'class':'form-control',
                  'style': 'width:16ch',
              }),
                  'numberOfLessons' : forms.NumberInput(attrs={
                  'placeholder':'Total',
                  'class':'form-control',
                  'style': 'width:16ch',
              }),
                  'packagePrice' : forms.NumberInput(attrs={
                  'placeholder':'Price',
                  'class':'form-control',
                  'style': 'width:16ch',
              }),
            } 


class assignPKGform(forms.ModelForm):
    #StudentId = forms.CharField(label=)
    #customerName = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    class Meta:
        model = AssignPackage
        fields = ('StudentId','packageName','startDate','endDate')
        endDate = forms.DateField(widget = forms.SelectDateWidget())
        labels = {'StudentId':'' , 'endDate' : 'End Date'
            }
        widgets = {
            'packageName': forms.Select(attrs={'placeholder': 'Package Name' , 'class':'form-control'}),
            'startDate': forms.DateInput(attrs={'class':'form-control'}),
            #'endDate': forms.DateInput(attrs={'class':'form-control'}),
            'StudentId':forms.Textarea(attrs={'hidden':'False'}),
        }

    def __init__(self,*args, **kwargs):
        super(assignPKGform, self).__init__(*args, **kwargs)
        self.fields['packageName'].queryset = studioPackages.objects.filter(active = True)
        self.fields['endDate'].widget = widgets.AdminDateWidget()

class PaymentForm(forms.ModelForm):
    #StudentId = forms.CharField(label=)
    #customerName = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    class Meta:
        model = customersPayments
        fields = ('transactionId','StudentId','Payment_Ref','transactionDate','paymenttype','paymentAmount','currency')
        labels = {'StudentId':''
            }
        widgets = {
            'Payment_Ref': forms.TextInput(attrs={'placeholder': 'Payment Ref', 'class':'form-control'}),
            'transactionDate': forms.DateInput(attrs={'class':'form-control'}),
            'paymenttype': forms.Select(attrs={'class':'form-control'}),
            'paymentAmount': forms.NumberInput(attrs={
                'class' : 'form-control',
                'id': 'number_field',
                'style': 'width:16ch',
                'placeholder':'Enter Amount'}),
            'StudentId':forms.Textarea(attrs={'hidden':'True'})
        }


class followUpForm(forms.ModelForm):
    class Meta:
        model = FollowUpModel
        fields = ('studentId','commentDate','comments','callBackOn','gb1')
        labels = {
            'studentId' : '',
            'commentDate' : 'Date',
            'comments' : 'comments',
            'callBackOn' : 'Call Back Date',
            'gb1' : 'Completed ?',
        }
        widgets = {'studentId': forms.HiddenInput()}
        Widget = {
            'packageName': forms.Select(attrs={'placeholder': 'Package Name' , 'class':'form-control'}),
            'commentDate': forms.DateInput(attrs={'class':'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'}),
            'comments':forms.Textarea(attrs={'class':'form-control'}),
        }


class checkInByUserForm(forms.ModelForm):
    #StudentId = forms.CharField(label=)
    #customerName = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    class Meta:
        model = checkInByUserModel
        fields = ('studentId','checkInValue')
        labels = {'studentId':'' }
        widgets = {
            'studentId':forms.Textarea(attrs={'hidden':'False'}),
        }

    def __init__(self,*args, **kwargs):
        super(checkInByUserForm, self).__init__(*args, **kwargs)
