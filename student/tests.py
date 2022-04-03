from django.test import TestCase

# Create your tests here.
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