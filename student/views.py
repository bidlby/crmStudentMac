




from django.shortcuts import redirect, render
from student.models import customerInfo 
from student.forms import newStudent , newCheckIn , derivePackageform , assignPKGform , PaymentForm
from django.contrib import messages
from rest_framework import generics
from django.views.generic import DetailView, UpdateView , ListView , TemplateView , CreateView
from .models import customerInfo , checkInData , studioPackages , groupAge , AssignPackage , leadSource , checkInByDateModel , customerPerformance , customerPaymentAccount , customersPayments
from .serializer import customerSerial 
from django.db.models import Count , Max , F , Min , Q , Sum
from django.db import connection
from django.urls import reverse, reverse_lazy
import datetime 
import time
from django.db.models.functions import Extract
from django.shortcuts import get_object_or_404  
from datetime import date, datetime, timedelta
from django.utils.timezone import now
import json
from django.db import connection




# Create your views here.

### Base ###

def base(request):
    return render(request,'student/base.html',{})

## home Page ##

class homePage(TemplateView):
    template_name = 'student/index.html'

class ReportsLinks(TemplateView):
    template_name = 'student/ReportsLinks.html'

##Vies##

class customerList(ListView): ## still not working
    queryset = customerInfo.objects.all()
    model = customerInfo
    serializer_class = customerSerial


    def list(request):
        queryset = customerInfo.objects.all()
        context = {'queryset':queryset}
        return render(request,'student/customerList.html',context)

def list(request):
    queryset1 = customerInfo.objects.all()
    query2 = customerInfo.objects.all().values('studentId').annotate(total=Count('studentId'))
    query3 = checkInData.objects.all()
    query4 = customerInfo.objects.raw(
       'SELECT a.studentid , a.customerName , count(b.checkIn) as count FROM STUDENT_customerInfo a ,student_checkindata b where a.studentid = b.studentid group by a.studentid , a.customerName')
    lastLogin = checkInData.objects.raw('select checkInSeq , a.studentid , max(a.checkInDate) from student_checkindata a group by a.studentid')
    context = {'q1':queryset1,'q2':query2,'q3':query3,'q4':query4,'lastLogin':lastLogin}
    return render(request,'student/customerList.html',context)


## Forms ## 
def NewReg(request):
    if request.method == 'POST':
        Reg_form = newStudent(request.POST)
        if Reg_form.is_valid():
            Reg_form.save()
            pass  # does nothing, just trigger the validation
    else:
        messages.error(request, 'Error saving form')

    Reg_form = newStudent()
    NewStud = customerInfo.objects.all()
    context = {'Reg_form':Reg_form,
                'NewStud':NewStud}
    return render(request,'student/NewReg.html', context)

## check In Form
def CheckInForm(request):
    if request.method == 'POST':
        checkIn_form = newCheckIn(request.POST)
        if checkIn_form.is_valid():
            checkIn_form.save()
            return redirect(reverse('student:successpage'))
    else:
        messages.error(request, 'Error saving form')

    checkIn_form = newCheckIn()
    Newcheck = checkInData.objects.all()
    context = {'checkIn_form':checkIn_form,
                'Newcheck':Newcheck}
    #return redirect(request,'student/homePage.html')
    return render(request,'student/checkIn.html', context)

def successpage(request):
    return render(request,'student/checkInPassed.html')

        
## check In by Name
def CheckInFormByName(request):
    if request.method == 'POST':
        checkIn_form = newCheckIn(request.POST)
        if checkIn_form.is_valid():
            checkIn_form.save()
            return redirect(reverse('student:successpage'))
    else:
        messages.error(request, 'Error saving form')

    checkIn_form = newCheckIn()
    Newcheck = checkInData.objects.all()
    context = {'checkIn_form':checkIn_form,
                'Newcheck':Newcheck}
    #return redirect(request,'student/homePage.html')
    return render(request,'student/checkInByName.html', context)

def successpage(request):
    return render(request,'student/checkInPassed.html')

##detailed View

class customerDtlView(DetailView):
    model = customerInfo
    fields = '__all__'

    def listdtl(request,pk):
        queryset = customerInfo.objects.filter(studentId=1)
        context = {'queryset':queryset}
        return render(request,'student/customerinfo_detail.html',context)

class customerViewUpdate(UpdateView):
    model = customerInfo
    fields = '__all__'
    

def detail_viewx(request, id):
    # dictionary for initial data with
    # field names as keys
    
 
    # add the dictionary during initialization
    idfilter  = checkInData.studentId = id
    
    data = customerInfo.objects.get(studentId = id)
    
    today = date.today()
    qw = checkInData.objects.filter(checkInDate__day=today.day).filter(studentId = id)
    bees = checkInData.objects.filter(studentId = id).count()
    xx = checkInData.objects.filter(studentId = id).first()
    checkinbydate = checkInData.objects.filter(studentId = id).filter(checkInDate__day=today.day).first()
    aa = checkInData.objects.filter(studentId = id).last()
    cc = datetime(2019, 10, 21) - datetime(2021,10,1)
    vv = checkInData.objects.values('studentId').annotate(maxdate=Max('checkInDate')).filter(studentId = id)
    #test = new_func1(id, today)
    vv2 = vv

    activePackage = AssignPackage.objects.raw("select b.PakageName as PKGName , b.numberOfLessons as totalLessons, a.soldPackageId , a.studentid_ID , a.packageName_ID as id2 from student_AssignPackage a , student_studioPackages b where a.packageName_id = b.packageId and a.studentId_id = %s ",[id])
    totalClass = AssignPackage.objects.raw("select sum(b.numberOfLessons) as totalLessons, a.soldPackageId from student_AssignPackage a , student_studioPackages b  where a.packageName_id = b.packageId and a.studentId_id = %s group by studentId_id",[id])
    sql = checkInData.objects.raw('select checkInSeq , sum(checkIn) as total from student_checkIndata where studentId = %s group by studentId',[id])

    remaingclass = AssignPackage.objects.raw("select a.soldPackageId ,  a.studentId_id ,  sum(distinct b.numberOfLessons) as total, sum(c.checkin)  as remaining from student_AssignPackage a , student_studioPackages b , student_checkInData c  where a.studentId_id = c.studentId and  a.packageName_id = b.packageId and a.studentId_id = %s group by a.studentId_id",[id])

    packA = AssignPackage.objects.filter(StudentId_id = id)

    cursor = connection.cursor()
    cursor2 = connection.cursor()
    xxc = cursor.execute("select sum(b.numberOfLessons) as total from student_AssignPackage a , student_studioPackages b  where  a.packageName_id = b.packageId and a.studentId_id = %s group by a.studentId_id",[id])
    xxc2 = cursor2.execute("select sum(checkIn) as total from student_checkInData  where  studentId = %s group by studentId",[id])
    qwe = cursor.fetchone()
    qwe2 = cursor2.fetchone()
    try:
        cursor.execute(xxc)
        qwe = cursor.fetchone([0])
    except Exception as e:
        cursor.close
        #
    try:
        cursor.execute(xxc2)
        qwe2 = cursor.fetchone()
        
    except Exception as e:
        cursor.close

    try:
        x1 = int(qwe[0])
    except Exception as e:
        x1 = 0

    try:
        x2 = int(qwe2[0])
    except Exception as e:
        x2 = 0

    
    try:
        final = x1 - x2
    except Exception as e:
        final = 0 

    final = x1 - x2


    context = {'data':data,'bees':f"{bees}",'xx':xx,'aa':aa,'cc':cc,'today':today,
    'qw':qw ,'vv':vv,'vv2':vv2,'sql':sql,'idfilter':idfilter,'activePackage':activePackage,
    'totalClass':totalClass,'remaingclass':remaingclass,'xxc':xxc,'qwe':qwe,'xxc2':xxc2,
    'qwe2':qwe2 , "final":final , 'x1':x1 , 'x2':x2 ,'packA':packA
        }
    return render(request, "student/dtl_multi.html", context)



#### Search funchion ####

def searchStudent(request):
    if request.method == "POST":
        searched = request.POST['searched']
        customerfilter = customerInfo.objects.filter(Q(studentId = searched)|Q(customerName__contains = searched))
        return render(request,'student/student_search.html',{'searched':searched,'filter':customerfilter})
    else :
        return render(request,'student/student_search.html',{})

def searchbyId(request):
    if request.method == "POST":
        searched = request.POST['searchID']
        customerfilter = customerInfo.objects.filter(Q(studentId = searched))
        return render(request,'student/SearchID.html',{'searchID':searched,'filter':customerfilter})
    else :
        return render(request,'student/SearchID.html',{})

### create view ###

class xx(CreateView):
    model = customerInfo
    form_class = newStudent
    #fields = '__all__'
    template_name = 'student/newLead.html'
    
    def get_success_url(self):
        return reverse('home')


#### New Package Form

class derivedPackage(CreateView):

    queryset = studioPackages.objects.all()

    model = studioPackages
    form_class = derivePackageform
    #fields = '__all__'
    initial = {'PakageName': ''}
    template_name = 'student/createPkg.html'
    
    
    
    def get_success_url(self):
        return reverse('student:home')

### age Group form

class createAgeList(CreateView):
    model = groupAge
    #form_class = derivePackage
    fields = '__all__'
    template_name = 'student/groupAge.html'
    
    def get_success_url(self):
        return reverse('student:home')

class leadSouceView(CreateView):
    model = leadSource
    #form_class = derivePackage
    fields = '__all__'
    template_name = 'student/NewLeadSource.html'

    def get_context_data(self, **kwargs):
       context = super(leadSouceView, self).get_context_data(**kwargs)
       context['queryset'] = leadSource.objects.all()
       return context

    def get_success_url(self):
        return reverse('home')

### Payments :

class CreatePayment(CreateView):
    model = customersPayments
    form_class = PaymentForm
    #fields = '__all__'
    template_name = 'student/AddPayment.html'

    def get_initial(self):
        StudentId = get_object_or_404(customerInfo, pk=self.kwargs['pk'])

        return {
        'StudentId': StudentId,
        }  

    def get_context_data(self, **kwargs):
       context = super(CreatePayment, self).get_context_data(**kwargs)
       context['queryset'] = customerInfo.objects.filter(pk=self.kwargs['pk'])
       return context

    def get_success_url(self):
        return reverse('student:soa')


## Assign Package:
class assignPKG(CreateView):
    model = AssignPackage
    form_class = assignPKGform
    #fields = '__all__'
    template_name = 'student/assignPKG.html'

    def get_initial(self):
        StudentId = get_object_or_404(customerInfo, pk=self.kwargs['pk'])

        return {
        'StudentId': StudentId,
        }

    def get_context_data(self, **kwargs):
       context = super(assignPKG, self).get_context_data(**kwargs)
       context['queryset'] = customerInfo.objects.filter(pk=self.kwargs['pk'])
       return context



    def get_success_url(self):
        return reverse('student:home')


class studentUpdateView(UpdateView):
    model = customerInfo
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('student:CustList')


## db view

def dbview(request):
    cur_date=now().date()-timedelta(days=1)
    cur_month=datetime.now().month
    cur_name_month = datetime.today()
    cur_name_month.strftime(('%B'))
    #cur_date = date(2022,1,1)-timedelta(days=1)
    a = checkInByDateModel.objects.filter(checkInDate=cur_date)
    b = checkInByDateModel.objects.filter(checkInDate__month=cur_month)

    newView = customerPerformance.objects.filter()

    context = {'a':a,'b':b,'cur_date':cur_date,'cur_month':cur_month,'cur_name_month':cur_name_month,'newView':newView}
    return render(request,'student/testdbvew.html',context)

## customer Account Balance 

def customerSOASummary(request):
    queryset1 = customerPaymentAccount.objects.all()
    queryset = customerPaymentAccount.objects.values('customerName','studentId').annotate(credit = Sum('credit')).annotate(debit=Sum('debit')).annotate(openBalance=F('credit') - F('debit')).annotate(lastTrx = Max('transactionDate'))

    TotalCredit = customerPaymentAccount.objects.aggregate(credits = Sum('credit'))
    Totaldebit = customerPaymentAccount.objects.aggregate(debits = Sum('debit'))
    TotalOpenAmount = customerPaymentAccount.objects.annotate(OpenAmount = F('credit') - F('debit'))

    try:
        openBalance = queryset['credit'] - queryset['debit']
    except Exception as e:
        openBalance = 0 
    
    try:
        xxx = TotalOpenAmount['OpenAmount']
    except Exception as e:
        xxx = 'None'


    context = {'queryset':queryset,'TotalCredit':TotalCredit,'Totaldebit':Totaldebit,'TotalOpenAmount':TotalOpenAmount,'openBalance':openBalance,'xxx':xxx}
    return render(request,'student/soa_summry.html',context)

def customerSOA(request,pk):
    queryset = customerPaymentAccount.objects.filter(studentId = pk)
    customerName = customerInfo.objects.filter(studentId = pk)
    totalCredit = customerPaymentAccount.objects.filter(studentId = pk).aggregate(credit = Sum('credit'))
    totalDebit = customerPaymentAccount.objects.filter(studentId = pk).aggregate(debit = Sum('debit'))

    try:
        openBalance = totalCredit['credit'] - totalDebit['debit']
    except Exception as e:
        openBalance = 0 

    
    context = {'queryset':queryset,'customerName':customerName,
               'openBalance':openBalance , 'totalCredit':totalCredit , 'totalDebit':totalDebit}
    return render(request,'student/soa.html',context)
