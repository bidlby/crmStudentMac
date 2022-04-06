import datetime
from django.db import NotSupportedError, models
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import now





# Create your models here.
class courseList(models.Model):
    coursList = models.CharField(max_length=50,unique=True)

    def __str__(self) -> str:
        return f'{self.coursList}'

class leadSource(models.Model):
    sourceChannel = models.CharField(max_length=50,unique=True)

    def __str__(self) -> str:
        return f'{self.sourceChannel}'

class countryList(models.Model):
    countryList = models.CharField(max_length=200 , unique=True)

    def __str__(self) -> str:
        return f'{self.countryList}'

class customerInfo(models.Model):
    studentId = models.AutoField(primary_key=True)
    customerName = models.CharField(max_length=100 , unique=True)
    customerImg = models.ImageField(upload_to ='media/student/imgs/' , default='default.jpg')
    leadsChannel = models.ForeignKey(leadSource,max_length=50,on_delete=models.CASCADE)
    adsRef = models.CharField(max_length=200,blank=True)
    contactDate = models.DateField(default=datetime.now , editable=False)
    leadeAge = models.IntegerField()
    leadsLocation = models.CharField(max_length=100)
    leadsContactNumber = models.IntegerField()
    emailAddress = models.EmailField(unique=True)
    leadsComment = models.CharField(max_length=1000)
    leadsUrgent = models.BooleanField()
    Nationality = models.ForeignKey(countryList,max_length=250,on_delete=models.CASCADE)
    intersetList = models.ForeignKey(courseList,max_length=50,on_delete=models.CASCADE)
    followUp = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.customerName}"
    

## customer Follow Up
class FollowUpModel(models.Model):
    commentSeq = models.AutoField(primary_key=True)
    studentId = models.ForeignKey(customerInfo,on_delete=models.DO_NOTHING)
    commentDate = models.DateField(default=datetime.now)
    comments = models.CharField(max_length=200)
    callBackOn = models.DateField()
    gb1 = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.studentId} , {self.comments}"

class checkInData(models.Model):
    checkInSeq = models.AutoField(primary_key=True)
    studentId = models.IntegerField()
    checkIn = models.IntegerField(default=1 , editable=False)
    checkInDate = models.DateField(default=datetime.now , editable=False)

    def __str__(self) -> str:
        return f"{self.studentId , self.checkIn , self.checkInDate}"

class groupAge(models.Model):
    groupAge = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.groupAge}"

class studioPackages(models.Model):
    packageId = models.AutoField(primary_key=True)
    PakageName = models.CharField(max_length=255, unique=True)
    courseName = models.ForeignKey(courseList,max_length=50,on_delete=models.CASCADE)
    group_age = models.ForeignKey(groupAge,max_length=255,on_delete=models.CASCADE)
    numberOfLessons = models.IntegerField()
    packagePrice = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.PakageName}"

class AssignPackage(models.Model):
   soldPackageId = models.AutoField(primary_key=True)
   transactionDate = models.DateField(default=datetime.now)
   StudentId = models.ForeignKey(customerInfo,max_length=255,on_delete=models.DO_NOTHING)
   packageName = models.ForeignKey(studioPackages,max_length=255,on_delete=models.DO_NOTHING)
   startDate = models.DateField(default=datetime.now)
   endDate = models.DateField(blank=True)

   def __str__(self) -> str:
       return f"{self.StudentId} , {self.packageName} , {self.soldPackageId}"

## Payment 



### db view

###
class checkInByDateModel(models.Model):
    checkInDate = models.DateField(editable=False , primary_key=True)
    total_checkIn = models.IntegerField(editable=False)

    def save(self,*args,**kwargs):
        raise NotSupportedError('this model view and cant be saved')

    class Meta:
       managed = False
       db_table = 'checkInbyDate'
       verbose_name = 'checkInTotal'
       verbose_name_plural = 'checkInTotals'
       ordering = ['checkInDate']

    def __str__(self) -> str:
       return f"{self.checkInDate} , {self.total_checkIn}"
###


class customerPerformance(models.Model):
    studentId = models.IntegerField(editable=False , primary_key=True)
    customerName = models.CharField(editable=False,max_length=100)
    countryList = models.CharField(editable=False , max_length=100)
    sourceChannel = models.CharField(editable=False , max_length=100)
    total_checkIn = models.IntegerField(editable=False)

    def save(self,*args,**kwargs):
        raise NotSupportedError('this model view and cant be saved')

    class Meta:
       managed = False
       db_table = 'customerPerformance'
       verbose_name = 'customerPerformance'
       verbose_name_plural = 'customerPerformances'
       ordering = ['studentId']

    def __str__(self) -> str:
       return f"{self.studentId} , {self.customerName} , {self.countryList} , {self.sourceChannel} , {self.total_checkIn}"
###


    ## Payments ##

class customersPayments(models.Model):

   # Payment Choices
   payType = [
        ('Card', 'Card'),
        ('Cash', 'Cash')
        ]

   transactionId = models.AutoField(primary_key=True)
   StudentId = models.ForeignKey(customerInfo,max_length=20,on_delete=models.DO_NOTHING)
   Payment_Ref = models.CharField(max_length=200)
   transactionDate = models.DateField(default=datetime.now)
   paymenttype = models.CharField(max_length=50, choices = payType , default='Cash')
   paymentAmount = models.IntegerField()
   currency = models.CharField(max_length=20 , default='AED')
   GB1 = models.BooleanField(default=False)

   def __str__(self) -> str:
       return f"{self.transactionId} Trx ID, {self.StudentId} , {self.paymentAmount} , {self.transactionDate}"


class customerPaymentAccount(models.Model):
    transactionDate = models.DateField(editable=False)
    studentId = models.IntegerField(editable=False , primary_key=True)
    customerName = models.CharField(editable=False,max_length=100)
    paymenttype = models.CharField(editable=False , max_length=50)
    Payment_Ref = models.CharField(editable=False , max_length=200)
    credit = models.IntegerField(editable=False)
    debit = models.IntegerField(editable=False)

    def save(self,*args,**kwargs):
        raise NotSupportedError('this model view and cant be saved')

    class Meta:
       managed = False
       db_table = 'CustomerAccountBalance'
       verbose_name = 'CustomerAccountBalance'
       verbose_name_plural = 'CustomerAccountBalances'
       ordering = ['transactionDate']

    def __str__(self) -> str:
       return f"{self.studentId} , {self.customerName} , {self.transactionDate} , {self.paymenttype} "
###