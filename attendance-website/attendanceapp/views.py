from django.shortcuts import render
from attendanceapp.models import Subteam, HoursWorked, Student
from django.http import HttpResponse
from django.utils import timezone
from django.template import RequestContext, loader
import math

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

    print (timeNow-lastLoggedIn).total_seconds

    print type((timeNow-lastLoggedIn).total_seconds)

    minutesWorked=float((timeNow-lastLoggedIn).total_seconds())
    minutesWorked=minutesWorked/60

    timeWorked=HoursWorked(timeIn=lastLoggedIn,timeOut=timeNow, totalTime=minutesWorked)
    timeWorked.save()

    student.hoursWorked.add(timeWorked)
    student.totalTime+=minutesWorked
    student.save()

    return minutesWorked

#Documentation needed

def logInPage(request):
    try: studentID=request.POST['studentID']
    except: return render(request, 'attendanceapp/ScanCard.html')
    student=Student.objects.get(studentID=studentID)
    if student.atLab==True:

        minutes = logOut(student)
        timeReturn = str(math.trunc(minutes/60)) + " hours, " + " and " + str(math.trunc(minutes%60)) + " minutes."
        return render(request,'attendanceapp/ScanCard.html',{'message':"Hello " + student.name + ". You worked " + timeReturn + " today."})

    else:
        logIn(student)
        return render(request,'attendanceapp/ScanCard.html',{'message':"Hello " + student.name + " you just logged in"})
