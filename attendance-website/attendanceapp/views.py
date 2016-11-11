from django.shortcuts import render
from attendanceapp.models import Subteam, HoursWorked, Student
from django.http import HttpResponse
from django.utils import timezone
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from operator import itemgetter

import math
import urllib2
import re

# Create your views here.

#idNotFound =  render(request, 'attendanceapp/ScanCard.html', {'message':"Sorry, student ID# not found."})
#helloMartin = render(request, 'attendanceapp/ScanCard.html', {'message':"Hi Martin!"})

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

    try:
        html = requests.post("https://palo-alto.edu/Forgot/Reset.cfm",data={"username":str(ID)}).text
        name = re.search(r'<input name="name" type="hidden" label="name" value="(.*?)"',html).group(1)
        Student(name=name,studentID=ID,subteam=Subteam.objects.get(name="Unknown")).save()
	return True
    except:
        return False


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
@login_required
def viewPeopleInfo(request, chartID = "chart_ID", chart_type = "column", chart_height = 500):
	names, hours = check_data()
	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
	title = {"text": "Student Hours"}
	xAxis = {"categories": names, "labels": {"rotation": 90}}
	yAxis = {"title": {"text": 'Hours'}}
	series = [
		{'name': 'Hours', 'data': hours}
	]
	return render(request, 'attendanceapp/viewPeopleHours.html', {'chartID': chartID, 'chart': chart,
                                                    'series': series, 'title': title, 
                                                    'xAxis': xAxis, 'yAxis': yAxis})

def viewPersonInfo(request):
    student = Student.objects.get(studentID = int(request.POST['id']))
    #return render(request,"attendanceapp/viewPersonInfo.html",{"name":student.name,"subteam":student.subteam.name,"hours":[i.timeIn,i.timeOut,i.totalTime for i in student.hoursWorked]})
	
def check_data():
	data = {}
	sorteddata = {}
	names = []
	hours= []
	students = Student.objects.all()
	for student in students:
		#data['name'].append(str(student.name))
		#data['hours'].append(student.totalTime/60)
		names.append(str(student.name))
		hours.append(student.totalTime/60)
		data = zip(names, hours)
	sorteddata = zip(*sorted(data, key=itemgetter(1), reverse=True))
	names = list(sorteddata[0])
	hours = list(sorteddata[1])
	return names, hours