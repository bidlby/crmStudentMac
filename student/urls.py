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


from django.urls import path, re_path 
from . import views
from django.views.generic import RedirectView
from django.views.static import serve 

app_name = 'student'

urlpatterns = [
    path('',RedirectView.as_view(url='accounts/login')),
    path('base',views.base,name='base'),
    path('home/',views.followup,name = 'home'),
    path('NewReg/',views.NewStudentReg.as_view(),name='NewReg'),
    path('list/',views.customerList.as_view(),name='CustList'),
    path('list2/',views.list,name='CustInfo2'),
    path('checkIn/',views.CheckInForm,name='checkIn'),
    path('customerDtl/<int:pk>',views.customerDtlView.as_view()),
    path('customerUpd/<int:pk>',views.customerViewUpdate.as_view()),
    path('successpage/',views.successpage,name='successpage'),
    path('student/dashBoard/<int:id>',views.detail_viewx),
    path('search',views.searchStudent,name='search'),
    path('searchID',views.searchbyId,name='searchID'),
    path('newPKG/',views.derivedPackage.as_view(),name='createPKG'),
    path('ageGroup/',views.createAgeList.as_view(),name='ageGroup'),
    path('list/assignPKG/<int:pk>',views.assignPKG.as_view(),name='assignPKG'),
    path('newLeadSouce/',views.leadSouceView.as_view(),name='NewSource'),
    path('list/updateView/<int:pk>',views.studentUpdateView.as_view(),name='updateView'),
    path('dbvew/',views.dbview,name='dbview'),
    path('ReportsLinks',views.ReportsLinks.as_view(),name='ReportsLinks'),
    path('list/soa/<int:pk>',views.customerSOA,name='soa_PK'),
    path('soa2/',views.customerSOA2,name='soa2'),
    path('soa_group/',views.customerSOASummary,name='soa'),
    path('AddPayment/<int:pk>',views.CreatePayment.as_view(),name= 'AddPayment'),
   #path('CheckInByName',views.CheckInFormByName,name='CheckInByName'),
    path('checkPost',views.checkPost,name='checkPost'),
    path('CheckInByName/',views.checkInName,name='CheckInByName'),
    path('checkPostName/',views.CheckInByName.as_view(),name='checkPostName'),
    path('customerFollowUp/',views.customerFollowUp,name='customerFollowUp'),
    path('student/editPackages/<int:pk>',views.editDerivedPackage.as_view(),name='editPackages'),
    path('pakcageList/',views.packageList,name='pakcageList'),
    path('pakcageReport/',views.pakcageReport , name='pakcageReport'),
    path('customerAttendance/',views.customerAttendance , name='customerAttendance'),
    path('testAny',views.testAny,name='testAny'),
    path('updateFollowFlag/<int:pk>',views.updateFollowFlag,name='updateFollowFlag'),
    path('dailyReports/',views.dailyReports,name='dailyReports'),
    path('toDolist/',views.toDolist,name='toDolist'),
    path('list/followUpView/<int:pk>',views.followUpView.as_view(),name='followUpView'),
    path('freetryList/',views.freetryList,name='freetryList'),
    path('py/',views.testAny,name='py'),



]
