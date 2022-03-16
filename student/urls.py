"""crmStudentMac URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.views import View
from . import views

app_name = 'student'

urlpatterns = [
    path('base',views.base,name='base'),
    path('',views.homePage.as_view(),name = 'home'),
    path('NewReg/',views.NewReg,name='NewReg'),
    path('list/',views.customerList.as_view(),name='CustList'),
    path('list2/',views.list,name='CustInfo2'),
    path('checkIn/',views.CheckInForm,name='checkIn'),
    path('customerDtl/<int:pk>',views.customerDtlView.as_view()),
    path('customerUpd/<int:pk>',views.customerViewUpdate.as_view()),
    path('successpage/',views.successpage,name='successpage'),
    path('dashBoard/<int:id>',views.detail_viewx),
    path('search',views.searchStudent,name='search'),
    path('searchID',views.searchbyId,name='searchID'),
    path('new/',views.xx.as_view()),
    path('newPKG/',views.derivedPackage.as_view(),name='createPKG'),
    path('ageGroup/',views.createAgeList.as_view(),name='ageGroup'),
    path('list/assignPKG/<int:pk>',views.assignPKG.as_view(),name='assignPKG'),
    path('newLeadSouce/',views.leadSouceView.as_view(),name='NewSource'),
    path('list/updateView/<int:pk>',views.studentUpdateView.as_view(),name='updateView'),
    path('dbvew/',views.dbview,name='dbview'),
    path('ReportsLinks',views.ReportsLinks.as_view(),name='ReportsLinks'),
    path('list/soa/<int:pk>',views.customerSOA,name='soa_PK'),
    path('soa_group/',views.customerSOASummary,name='soa'),
    path('AddPayment/<int:pk>',views.CreatePayment.as_view(),name= 'AddPayment'),
    path('CheckInByName',views.CheckInFormByName,name='CheckInByName')
]
