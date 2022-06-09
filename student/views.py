
import django
from django.shortcuts import redirect, render
from student.models import customerInfo 
from student.forms import newStudent , newCheckIn , derivePackageform , assignPKGform , PaymentForm , followUpForm , checkInByUserForm
from django.contrib import messages
from django.views.generic import DetailView, UpdateView , ListView , TemplateView , CreateView
from .models import customerInfo , checkInData , studioPackages , groupAge , AssignPackage , leadSource , checkInByDateModel , customerPerformance , customerPaymentAccount , customersPayments ,FollowUpModel , checkInByUserModel
from django.db.models import Count , Max , F , Min , Q , Sum
from django.db import connection
from django.urls import reverse, reverse_lazy
import datetime 
from django.shortcuts import get_object_or_404  
from datetime import date, datetime, timedelta
from django.utils.timezone import now
from django.db import connection
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required



# Create your views here.

### Base ###

def base(request):
    return render(request,'student/base.html',{})

## home Page ##

#class homePage(TemplateView):
    #template_name = 'student/index.html'
    
def followup(request):
        pkg_list = studioPackages.objects.filter(active = True)
        followUpList = customerInfo.objects.filter(followUp = True)
        a3 = 1
        q1 = 3


        if request.method == 'POST':
            age = request.POST['age']
            course = request.POST['course']
            age_filter = studioPackages.objects.select_related('group_age','courseName').values_list('group_age__groupAge','PakageName','courseName__coursList','numberOfLessons','packagePrice').filter(Q(group_age__groupAge__contains=age),Q(courseName__coursList__contains=course)).filter(active=True)
            context = {'age_filter':age_filter,'followUpList':followUpList}
            return render(request,'student/Index.html',context)
        else:
            age_filter = studioPackages.objects.select_related('group_age','courseName').values_list('group_age__groupAge','PakageName','courseName__coursList','numberOfLessons','packagePrice').all().filter(active=True)
            context = {'age_filter':age_filter,'followUpList':followUpList}
            return render(request,'student/Index.html',context)


        context = {'pkg_list':pkg_list,'followUpList':followUpList , 'q1':q1 , 'a3':a3}

        return render(request,'student/index.html',context)



        

class ReportsLinks(TemplateView):
    template_name = 'student/ReportsLinks.html'

##Vies##

class customerList(ListView): ## still not working
    queryset = customerInfo.objects.all()
    paginate_by = 5
    model = customerInfo
 


    def list(request):
        queryset = customerInfo.objects.all()
        context = {'queryset':queryset}
        return render(request,'student/customerList.html',context)

## Follow up View

def customerFollowUp(request):
    followList = customerInfo.objects.filter(followUp=True)
    context = {'followList':followList}
    return render(request,'student/customerinfo_followUp.html',context)

####

def list(request):
    queryset1 = customerInfo.objects.all()
    query2 = customerInfo.objects.all().values('studentId').annotate(total=Count('studentId'))
    query3 = checkInData.objects.all()
    query4 = customerInfo.objects.raw(
       'SELECT a.studentid , a.customerName , count(b.checkIn) as count FROM STUDENT_customerInfo a ,student_checkindata b where a.studentid = b.studentid group by a.studentid , a.customerName')
    lastLogin = checkInData.objects.raw('select checkInSeq , a.studentid , max(a.checkInDate) from student_checkindata a group by a.studentid')
    context = {'q1':queryset1,'q2':query2,'q3':query3,'q4':query4,'lastLogin':lastLogin}
    return render(request,'student/customerList.html',context)


## New Customer ## 

class NewStudentReg(CreateView):
    model = customerInfo
    form_class = newStudent
    #fields = '__all__'
    template_name = 'student/NewReg.html'
    
    def get_success_url(self):
        return reverse('student:CustList')

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

def checkInName(request):

    if request.method == 'POST':
        idFilter = request.POST['searchID']
        NameFilter = customerInfo.objects.filter(studentId = idFilter)
        context = {'NameFilter':NameFilter}
        #return reverse('student:checkPostName')
        return render(request,'student/checkInByNamePost.html',context)
    else:
        return render(request,'student/checkInByName.html',{})

def checkPost(request):
    return render(request,'student/checkInByNamePost.html',{})

### Payments :

class CheckInByName(CreateView):
    model = checkInData
    form_class = newCheckIn
    #fields = '__all__'
    template_name = 'student/checkInByNamePost.html'

    def get_success_url(self):
        return reverse('student:checkPostName')

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
    aPKG = customerInfo.objects.filter(studentId = id)

    
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
    'qwe2':qwe2 , "final":final , 'x1':x1 , 'x2':x2 ,'packA':packA,'aPKG':aPKG}
    return render(request, "student/dtl_multi.html", context)



#### Search function ####

def searchStudent(request):
    if request.method == "POST":
        searched = request.POST['searched']
        customerfilter = customerInfo.objects.filter(Q(studentId__contains = searched)|Q(customerName__contains = searched))
        return render(request,'student/student_search.html',{'searched':searched,'filter':customerfilter})
    else :
        return render(request,'student/student_search.html',{})

def searchbyId(request):
    if request.method == "POST":
        searched = request.POST['searchID']
        customerfilter = customerInfo.objects.filter(studentId = searched)
        return render(request,'student/student_search2.html',{'searchID':searched,'filter':customerfilter})
    else :
        return render(request,'student/student_search2.html',{})

### create view ###




#### New Package Form

class derivedPackage(CreateView):

    queryset = studioPackages.objects.all()

    model = studioPackages
    form_class = derivePackageform
    #fields = '__all__'
    initial = {'PakageName': ''}
    template_name = 'student/createPkg.html'
    
    def get_context_data(self, **kwargs):
       context = super(derivedPackage, self).get_context_data(**kwargs)
       context['packages'] = studioPackages.objects.all()
       return context
    
    def get_success_url(self):
        return reverse('student:home')

### Edit Packages

class editDerivedPackage(UpdateView):
    model = studioPackages
    form_class = derivePackageform
    #fields = '__all__'
    template_name_suffix = '_Update'
    success_url = reverse_lazy('student:createPKG')


def packageList(request):
    packageListAll = studioPackages.objects.all()
    context = {'packageListAll':packageListAll}
    return render(request,'student/packagelist.html',context)



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
    fields = '__all__'
    template_name = 'student/NewLeadSource.html'

    def get_context_data(self, **kwargs):
       context = super(leadSouceView, self).get_context_data(**kwargs)
       context['queryset'] = leadSource.objects.all()
       return context

    def get_success_url(self):
        return reverse('student:home')

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
    model = AssignPackage.objects.select_related('packageName_id').filter(packageName_id__active = False)
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
    template_name_suffix = '_update'
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

    queryset = customerPaymentAccount.objects.values('customerName','studentId').annotate(credit = Sum('credit')).annotate(debit=Sum('debit')).annotate(openBalance=F('credit') - F('debit')).annotate(lastTrx = Max('transactionDate')).exclude(openBalance = 0).order_by('-openBalance','lastTrx')

    customerOpenAmount = queryset.values('studentId')


    TotalCredit = customerPaymentAccount.objects.filter(studentId__in = customerOpenAmount).aggregate(credits = Sum('credit'))
    Totaldebit = customerPaymentAccount.objects.filter(studentId__in = customerOpenAmount).aggregate(debits = Sum('debit'))
    TotalOpenAmount = customerPaymentAccount.objects.aggregate(openAmount = Sum('credit') - Sum('debit'))

    print(TotalOpenAmount)
    

    try:
        openBalance = queryset['credit'] - queryset['debit']
    except Exception as e:
        openBalance = 0 
    
    try:
        xxx = TotalOpenAmount['balance']
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

    if request.method == 'POST':
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']
        showresult = customerPaymentAccount.objects.filter(transactionDate__gte=fromdate,transactionDate__lte=todate,studentId=pk).order_by('-transactionDate')

        context = {'queryset':queryset,'customerName':customerName,
               'openBalance':openBalance , 'totalCredit':totalCredit , 
               'totalDebit':totalDebit,'showresult':showresult}
        #showresult = customerPaymentAccount.objects.raw('select * student_customerspayments where transactionDate >= "'+fromdate+'" and transactionDate <= "'+todate+'" and studentId = %s' ,[pk])
        return render(request,'student/soa.html',context)
    else:
        showresult = customerPaymentAccount.objects.filter(studentId=pk).order_by('-transactionDate')
        context = {'queryset':queryset,'customerName':customerName,
               'openBalance':openBalance , 'totalCredit':totalCredit ,
                'totalDebit':totalDebit,'showresult':showresult}
        return render(request,'student/soa.html',context)

def customerSOA2(request):
    queryset = customerPaymentAccount.objects.all()
    customerName = customerInfo.objects.all()
    totalCredit = customerPaymentAccount.objects.all().aggregate(credit = Sum('credit'))
    totalDebit = customerPaymentAccount.objects.all().aggregate(debit = Sum('debit'))

    try:
        openBalance = totalCredit['credit'] - totalDebit['debit']
    except Exception as e:
        openBalance = 0 

    if request.method == 'POST':
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']
        #showresult = customerPaymentAccount.objects.raw('select * student_customerspayments where transactionDate >= "'+fromdate+'" and transactionDate <= "'+todate+'"')
        showresult = customerPaymentAccount.objects.filter(transactionDate__gte=fromdate,transactionDate__lte=todate)
        return render(request,'student/soa_f.html',{'showresult':showresult})
    else:
        showresult = customerPaymentAccount.objects.all() 
        context = {'queryset':queryset,'customerName':customerName,
               'openBalance':openBalance , 'totalCredit':totalCredit , 'totalDebit':totalDebit}
        return render(request,'student/soa_f.html',{'showresult':showresult})


### Packages Sold Report:

def pakcageReport(request):
    

    TotalPkgSaleMonhtly = AssignPackage.objects.annotate(month = TruncMonth('transactionDate')).values('month').annotate(tp = Count('packageName_id')).annotate(tm = Sum('packageName__packagePrice')).filter(packageName__packagePrice__gte = 1).order_by('-month')

    packageSoldTotal = AssignPackage.objects.filter(packageName__packagePrice__gte = 2).aggregate(tCount = Count('packageName_id'),tm = Sum('packageName__packagePrice'))


    if request.method == 'POST':

        fromdate = request.POST['fromdate']
        todate = request.POST['todate']

        packageSold2 = AssignPackage.objects.filter(transactionDate__gte=fromdate,transactionDate__lte=todate).select_related('packageName_id').values_list('packageName__PakageName','packageName__packagePrice','transactionDate').annotate(total=Count('packageName'),total_amount=Sum('packageName__packagePrice')).order_by('-transactionDate').filter(packageName__packagePrice__gte = 1)

        total_PKG = AssignPackage.objects.filter(transactionDate__gte=fromdate,transactionDate__lte=todate,packageName__packagePrice__gte = 1).aggregate(tCount = Count('StudentId'), tAmount = Sum('packageName__packagePrice'))

        context = {'total_PKG':total_PKG ,'packageSold2':packageSold2,
                    'TotalPkgSaleMonhtly' :TotalPkgSaleMonhtly,
                    'packageSoldTotal':packageSoldTotal}
        return render(request,'student/packageReport.html',context)
    else:
        today = date.today()

        packageSold2 = AssignPackage.objects.select_related('packageName_id').values_list('packageName__PakageName','packageName__packagePrice','transactionDate').annotate(total=Count('packageName'),total_amount=Sum('packageName__packagePrice')).order_by('-transactionDate').filter(packageName__packagePrice__gte = 1).filter(transactionDate__month = today.month , transactionDate__year = today.year)

        total_PKG = AssignPackage.objects.filter(packageName__packagePrice__gte = 1, transactionDate__month = today.month , transactionDate__year = today.year).aggregate(tCount = Count('StudentId'), tAmount = Sum('packageName__packagePrice'))

        context = {'total_PKG':total_PKG ,'packageSold2':packageSold2,
                    'TotalPkgSaleMonhtly':TotalPkgSaleMonhtly,
                    'packageSoldTotal':packageSoldTotal}
        return render(request,'student/packageReport.html',context)

### Performance Report :

def customerAttendance(request):

    totalCheckInMonthly = checkInData.objects.annotate(month = TruncMonth('checkInDate')).values('month').annotate(tCheck = Count('checkInSeq')).order_by('-month')
    checkInTotal = checkInData.objects.values('checkInDate').annotate(countCheck = Count('checkInSeq')).order_by('-checkInDate')

    conte = {'checkInTotal':checkInTotal,'totalCheckInMonthly':totalCheckInMonthly}
    return render(request,'student/checkInReport.html',conte)


## test to https://bees.pythonanywhere.com/checkIn/

def testAny(request):
    curMonth = date.today()

    return render(request,'student/testPyAnyWhere.html',{'curMonth':curMonth})


## update value 

def updateFollowFlag(request,pk):
    a = customerInfo.objects.filter(studentId = pk).update(followUp = False)

    return render(request,'student/zupdatex.html',{'a':a})


## to do list

def toDolist(request):

    NetClasses = customerPerformance.objects.raw('select c.studentId, c.customerName , sum(b.numberOfLessons) as total , c.total_checkIn , sum(b.numberOfLessons) - c.total_checkIn as net from student_AssignPackage a , student_studioPackages b , customerPerformance c  where  a.packageName_id = b.packageId and c.studentid = a.studentid_id and b.freeTry = 0 group by c.customerName , a.studentId_id order by sum(b.numberOfLessons) - c.total_checkIn asc')

    return render(request,'student/toDoList.html',{'NetClasses':NetClasses})

## follow Up View:

class followUpView(CreateView):
    model = FollowUpModel
    form_class = followUpForm
    template_name = 'student/followUpComment.html'

    def get_initial(self):
        studentId = get_object_or_404(customerInfo, pk=self.kwargs['pk'])

        return {
        'studentId': studentId,
        }

    def get_context_data(self, **kwargs):
       context = super(followUpView, self).get_context_data(**kwargs)
       context['queryset'] = customerInfo.objects.filter(pk=self.kwargs['pk'])
       context['commentList'] = FollowUpModel.objects.filter(studentId = self.kwargs['pk']).order_by('-commentSeq')

       return context

    def get_success_url(self):
        return reverse('student:followUpView')

### Reports:
def dailyReports(request):

    currDay = date.today()

    dailyCheckInReport = customerInfo.objects.raw(
       'SELECT b.checkInDate , a.studentid , a.customerName , count(b.checkIn) as count FROM STUDENT_customerInfo a ,student_checkindata b where a.studentid = b.studentid and checkInDate =  %s group by a.studentid , a.customerName , b.checkInDate',[currDay])

    ## Remianing Classes

    NetClasses = customerPerformance.objects.raw('select c.studentId, c.customerName , sum(b.numberOfLessons) as total , c.total_checkIn , sum(b.numberOfLessons) - c.total_checkIn as net from student_AssignPackage a , student_studioPackages b , customerPerformance c  where  a.packageName_id = b.packageId and c.studentid = a.studentid_id group by c.customerName , a.studentId_id order by sum(b.numberOfLessons) - c.total_checkIn asc')



    context = {'NetClasses':NetClasses,'dailyCheckInReport':dailyCheckInReport}

    return render(request,'student/zupdate.html',context)

## Sutdent Attendacnce report

def studendAttendanceReport(request,pk):

    currDay = date.today()

    studnetName = customerInfo.objects.get(studentId = pk)

    checkInDatebyStudent = checkInData.objects.filter(studentId= pk).values('checkInDate','studentId').order_by('-checkInDate')

    monthlyAttendanceReport = checkInData.objects.filter(studentId= pk).values('checkInDate').annotate(tCount = Count('checkInDate')).order_by('-checkInDate')
    

    monthlyAttendanceReport = checkInData.objects.filter(studentId= pk).values(month = TruncMonth('checkInDate')).annotate(tCount = Count('checkInDate')).order_by('-month')

    context = {'checkInDatebyStudent':checkInDatebyStudent , 'monthlyAttendanceReport':monthlyAttendanceReport,'studnetName':studnetName}

    return render(request,'student/studentAttendance.html',context)    


## Free Try Out :

@login_required
def freetryList(request):

    anyPkg = AssignPackage.objects.values('StudentId_id')
    pricedList = studioPackages.objects.filter(freeTry = True)


    studentPricedList = AssignPackage.objects.exclude(packageName__in = pricedList).values('StudentId')
    studentFreeList = AssignPackage.objects.filter(packageName__in = pricedList).values('StudentId')


    
    studentWithPricedPkg = customerInfo.objects.filter(studentId__in = studentPricedList)

    withNoPkg =  customerInfo.objects.exclude(studentId__in = anyPkg).filter(followUp = True)

    freeTryList = customerInfo.objects.exclude(studentId__in = studentWithPricedPkg).exclude(studentId__in = withNoPkg).filter(followUp = True)

    TotalFreeMonhtly = AssignPackage.objects.annotate(month = TruncMonth('transactionDate')).values('month').annotate(tp = Count('packageName_id')).filter(packageName__packagePrice = 0)

    feeListId = AssignPackage.objects.filter(StudentId__in = studentPricedList)


    totalPaidPkg = AssignPackage.objects.annotate(month = TruncMonth('transactionDate')).values('month').annotate(tFree = Count('transactionDate' , filter = Q(packageName__packagePrice = 0))).annotate(tPaid = Count('transactionDate' , filter = Q(packageName__packagePrice__gte = 1))).order_by('-month')
 
    totalPaidPkgx = AssignPackage.objects.annotate(month = TruncMonth('transactionDate')).values('month').annotate(tFree = Count('transactionDate' , filter = Q(packageName__packagePrice = 0))).annotate(tPaid = Count('transactionDate', filter = Q(StudentId__in = studentFreeList , packageName__packagePrice__gt = 1))).order_by('-month')


    context = {'freeTryList':freeTryList,'withNoPkg':withNoPkg,'TotalFreeMonhtly':TotalFreeMonhtly,'totalPaidPkg':totalPaidPkg,'totalPaidPkgx':totalPaidPkgx,'feeListId':feeListId}

    return render(request,'student/freeTry.html',context)

   
   ## checkInBySearch

   #### Search function ####

def checkInSearch(request):
    if request.method == "POST":
        searched = request.POST['checkInSearch']
        customerfilter = customerInfo.objects.filter(studentId = searched)
        context = { 'checkInSearch':searched,
                    'customerfilter':customerfilter }
        return render(request,'student/checkInSearchResult.html',context)
    else :
        return render(request,'student/checkInSearch.html',{})


class CheckInByName(CreateView):
    model = checkInByUserModel
    form_class = checkInByUserForm
    #fields = '__all__'
    template_name = 'student/checkInResultC.html'

    def get_initial(self):
        StudentId = get_object_or_404(customerInfo, pk=self.kwargs['pk'])

        return {
        'StudentId': StudentId,
        }

    def get_context_data(self, **kwargs):
       context = super(CheckInByName, self).get_context_data(**kwargs)
       context['queryset'] = customerInfo.objects.filter(pk=self.kwargs['pk'])
       return context


    def get_success_url(self):
        return reverse('student:home')
