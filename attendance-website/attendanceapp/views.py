from django.shortcuts import render
from attendanceapp.models import Subteam, HoursWorked, Student
from django.http import HttpResponse
from django.utils import timezone
from django.template import RequestContext, loader
import math

# Create your views here.

def index(request):
    template=loader.get_template('attendanceapp/index.html')
    #Load the index html page
    context=RequestContext(request)
    #build the data to put into the HTML page -> Right now there is nothing

    #Render the html and return it to the user -> This is only used in the index view
    return HttpResponse(template.render(context))

def logIn(student):
    student.atLab=True
    #make the student at the lab
    student.lastLoggedIn=timezone.now()
    #set the login time
    student.save()
    #write to the database

def logOut(student):
    student.atLab=False
    #tell the system that the student is no longer in the lab
    lastLoggedIn=student.lastLoggedIn
    #load the last logged in time into memory
    timeNow=timezone.now()
    #get the time now so we get the most accurate  time in relation to when they logged in

    #print (timeNow-lastLoggedIn).total_seconds

    #print type((timeNow-lastLoggedIn).total_seconds)

    #get the time they were in the lab and convert it from seconds to minutes
    minutesWorked=float((timeNow-lastLoggedIn).total_seconds())
    minutesWorked=minutesWorked/60
    
    #create the "Time worked" object to be added to the student database
    timeWorked=HoursWorked(timeIn=lastLoggedIn,timeOut=timeNow, totalTime=minutesWorked)
    timeWorked.save()

    #add the time worked object to the student so it can be viewed in the calander
    student.hoursWorked.add(timeWorked)
    
    #add the minutes to the student's total time
    student.totalTime+=minutesWorked
    
    student.save()
    #save the student object
    
    #return the number of minutes
    return minutesWorked



def logInPage(request):
    #check if we are passed the student ID -> check if it is first time loading the page
    #if this passes, that means a student is logging in/out
    #if this fails
    try: studentID=request.POST['studentID']
    
    except: 
        return render(request, 'attendanceapp/ScanCard.html')
    
    student=Student.objects.get(studentID=studentID)
    if student.atLab==True:

        minutes = logOut(student)
        timeReturn = str(math.trunc(minutes/60)) + " hours, " + " and " + str(math.trunc(minutes%60)) + " minutes."
        return render(request,'attendanceapp/ScanCard.html',{'message':"Hello " + student.name + ". You worked " + timeReturn + " today."})

    else:
        logIn(student)
        return render(request,'attendanceapp/ScanCard.html',{'message':"Hello " + student.name + " you just logged in"})
