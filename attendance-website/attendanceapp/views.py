from django.shortcuts import render
from attendanceapp.models import Subteam, HoursWorked, Student
from django.http import HttpResponse
from django.utils import timezone
from django.template import RequestContext, loader


# Create your views here.

def index(request):
    template=loader.get_template('attendanceapp/index.html')
    context=RequestContext(request)
    print 'Hi!'
    return HttpResponse(template.render(context))

def logIn(student):
    student.atLab=True
    student.lastLoggedIn=timezone.now()
    student.save()

def logOut(student):
    student.atLab=False

    lastLoggedIn=student.lastLoggedIn
    timeNow=timezone.now()

    minutesWorked=timeNow-lastLoggedIn
    minutesWorked=minutesWorked/60

    timeWorked=HoursWorked(timeIn=lastLoggedIn,timeOut=timeNow, totalTime=minutesWorked)
    timeWorked.save()

    student.hoursWorked.add(timeWorked)
    student.totalTime+=minutesWorked
    student.save()

    return minutesWorked

def logInPage(request):
    studentID=request.POST['studentID']
    student=Student.objects.get(studentID=studentID)
    if student.atLab==True:
        minutes = logOut(student)
        return "Hello " + student.name + ". You worked " + str(minutes) + " today."

    else:
        logIn(student)
        return "Hello " + student.name + " you just logged in."
