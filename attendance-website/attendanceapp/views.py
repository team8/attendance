from django.shortcuts import render
from attendanceapp.models import Subteam, HoursWorked, Student
from django.http import HttpResponse
from django.utils import timezone
from django.template import RequestContext, loader
import math

# Create your views here.

def index(request):
    #Load the index html page
    template=loader.get_template('attendanceapp/index.html')

    #Build the data to put into the HTML page -> Right now there is nothing
    context=RequestContext(request)

    #Render the html and return it to the user -> This is only used in the index view
    return HttpResponse(template.render(context))

def logIn(student):
    #Make the student at the lab
    student.atLab=True

    #Set the login time
    student.lastLoggedIn=timezone.now()

    #Write to the database
    student.save()

def logOut(student):
    #Tell the system that the student is no longer in the lab
    student.atLab=False

    #load the last logged in time into memory
    lastLoggedIn=student.lastLoggedIn

    #Get the time now so we get the most accurate  time in relation to when they logged in
    timeNow=timezone.now()

    #print (timeNow-lastLoggedIn).total_seconds

    #print type((timeNow-lastLoggedIn).total_seconds)

    #Get the time they were in the lab and convert it from seconds to minutes
    minutesWorked=float((timeNow-lastLoggedIn).total_seconds())
    minutesWorked=minutesWorked/60

    #Create the "Time worked" object to be added to the student database
    timeWorked=HoursWorked(timeIn=lastLoggedIn,timeOut=timeNow, totalTime=minutesWorked)
    timeWorked.save()

    #add the time worked object to the student so it can be viewed in the calander
    student.hoursWorked.add(timeWorked)

    #add the minutes to the student's total time
    student.totalTime+=minutesWorked

    #Save the student object
    student.save()


    #Return the number of minutes
    return minutesWorked

def logInPage(request):
    #Check if we are passed the student ID -> check if it is first time loading the page
    #If this passes, that means a student is logging in/out
    #If this fails...???
    try:
        studentID=request.POST['studentID']
    except:
        return render(request, 'attendanceapp/ScanCard.html', {'message':"Sorry, student ID# not found."})

    student=Student.objects.get(studentID=studentID)
    if student.atLab==True:

        minutes = logOut(student)
        timeReturn = str(math.trunc(minutes/60)) + " hours, " + " and " + str(math.trunc(minutes%60)) + " minutes." #This should be encapsulated
        return render(request,'attendanceapp/ScanCard.html',{'message':"Hello " + student.name + ". You worked " + timeReturn + " today."}, {'color':"#FF0000"}) #I don't know how much we can do about this though, sadly. I am currently passing another argument to render, "color". Since this is the logout method, it sets the background color to red. I am trying to see if I can use this to set the background color of the page via CSS. This is probably not the proper way to do it, but it's 3AM and I should really sleep.

    else:
        logIn(student)
        return render(request,'attendanceapp/ScanCard.html',{'message':"Hello " + student.name + ", you just logged in"}, {'color':"#32CD32"}) #This *should* set the background color to lime green, to indicate that they have successfully logged in. Again, this is a "hack", let's see if I know what I'm doing.

#This is part of our Slack Integration. This one is supposed to return a list of people currently in the lab. SLack will send a payload through POST, we have to interpret it and send a response back. Not implemented (yet).
def whoIsInLab(request):
    try:
        pass
    except Exception as e:
        raise


#This is part of our Slack Integration. Same technical details as above, this one will return true/false depending on whether the specific person requested is in the lab or not. Not implemented (yet).
def specificPersonInLab(request):
    try:
        ID = request.POST['studentID']
    except KeyError:
        return
    student=Student.objects.get(studentID=ID)
