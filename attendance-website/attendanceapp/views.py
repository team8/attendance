from django.shortcuts import render
from attendanceapp.models import Subteam, HoursWorked, Student
from django.http import HttpResponse
from django.utils import timezone
from django.template import RequestContext, loader

import math
import urllib2
import re
import requests
# Create your views here.

#idNotFound =  render(request, 'attendanceapp/ScanCard.html', {'message':"Sorry, student ID# not found."})
#helloMartin = render(request, 'attendanceapp/ScanCard.html', {'message':"Hi Martin!"})
def eHash(x):
        x = str(x)
        y=[ord(z) for z in x]
        if len(x) != 0:
                x = y[0]
                z = 1
                while z != len(y):
                        x = x * y[z] ** z
                        z = z + 1
                x = str(x)
                x = [x[i:i+2] for i in range(0, len(x), 2)]
                z = ''
                for y in x: z = z + chr(int(y))
                print z
                return z


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


def makeNewStudent(ID):
	html = requests.post("https://palo-alto.edu/Forgot/Reset.cfm",data={"username":str(ID)}).text
	try:name = re.search(r'<input name="name" type="hidden" label="name" value="(.*?)"',html).group(1)
	except:return False
	Student(name=name,studentID=ID,subteam=Subteam.objects.get(name="Unknown")).save()
	return True

def logInPage(request):
    #Check if we are passed the student ID -> check if it is first time loading the page
    #If this passes, that means a student is logging in/out
    #If this fails...???

    try: studentID=request.POST['studentID']
    except: return render(request, 'attendanceapp/ScanCard.html')

    #if len(studentID)==4:
    #    if studentID=="8888":
    #        #return helloMartin
    #    else: return idNotFound

    #Check to see if the inputted # meets the standard for ID# format. This
    #should be encapsulated, but it may be redundant with the introduction of
    #the HTML5 pattern attribute on the ScanCard page.
    if len(studentID) != 8:
        if len(studentID)==14:
            studentID=studentID[5:13]
        else: return idNotFound

    try: student=Student.objects.get(studentID=studentID)

    except:
        if makeNewStudent(request.POST['studentID']) == False:
            print "makeNewStudent failing"
            return render(request, 'attendanceapp/ScanCard.html', {'message':"Sorry, student ID# not found."})
        else:
            student=Student.objects.get(studentID=studentID)


    if student.atLab==True:

        minutes = logOut(student)
        timeReturn = str(math.trunc(minutes/60)) + " hours, " + " and " + str(math.trunc(minutes%60)) + " minutes"
        return render(request,'attendanceapp/ScanCard.html',{'message':"Hey " + student.name + "! You worked " + timeReturn + ", great job!"})

    else:
        logIn(student)
        return render(request,'attendanceapp/ScanCard.html',{'message':"Hey " + student.name + ", you just logged in. Good to see you!"})

#This is part of our Slack Integration.
#This one is supposed to return a list of people currently in the lab.
#Slack will send a payload through POST.
#We have to interpret it and send a response back. Not implemented (yet).
def whoIsInLab(request):
    try:
        pass
    except Exception as e:
        raise


#This is part of our Slack Integration.
#Same technical details as above, this one will return true/false depending on whether the specific person requested is in the lab or not. Not implemented (yet).
def specificPersonInLab(request):
    try:
        ID = request.POST['studentID']
    except KeyError:
        return
    student=Student.objects.get(studentID=ID)

def viewPeoplePWPage(request):
    print request.POST
    return render(request, "attendanceapp/viewPeoplePwPage.html")

def viewPeopleInfo(request):
    # print "HELLO!!!!"
    # print request.POST["password"]
    # if request.POST['password'] == "thepassword":
        students = []
        for student in Student.objects.all():
            students.append([student.name,student.subteam.name,student.totalTime/60,student.studentID,[[i.timeIn,i.timeOut,i.totalTime/60] for i in student.hoursWorked.all()]])
        return render(request,"attendanceapp/viewPeopleHours.html",{"peopleInfo":students})
    # else: return viewPeoplePWPage(request)

def viewPersonInfo(request):
    student = Student.objects.get(studentID = int(request.POST['id']))
    #return render(request,"attendanceapp/viewPersonInfo.html",{"name":student.name,"subteam":student.subteam.name,"hours":[i.timeIn,i.timeOut,i.totalTime for i in student.hoursWorked]})

def login(request):
    return render(request,"attendanceapp/loginPage.html")

def viewHours(request):
    try:
        student = Student.objects.get(studentID=request.POST["Student ID"])
    except:
            return render(request,"attendanceapp/loginPage.html",{"msg":"Student Not found"})

    if eHash(student.password) != eHash(request.POST["password"]):
        return render(request,"attendanceapp/loginPage.html",{"msg":"Student Not found"})

    #return render(request,"attendanceapp/studentLogin.html",{"totalHours":student.totalTime/60,"days":,[[i.timeIn,i.timeOut,i.totalTime/60] for i in student.hoursWorked.all()]})
