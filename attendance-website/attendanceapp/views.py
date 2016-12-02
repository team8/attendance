from django.shortcuts import render
from attendanceapp.models import Subteam, HoursWorked, Student, LabHours, OverallStats
from django.http import HttpResponse
from django.utils import timezone
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from operator import itemgetter
from forms import SubteamForm
from attendanceapp.tables import StudentTable, StatTable
from django_tables2 import RequestConfig
from datetime import datetime, timedelta
from util import check_data, convertTime, weighted_average_and_stddev, student_overall_stats, get_total_days, get_percent_days, most_frequent_day

import math
import urllib2
import re

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


def logOut(student, save, autolog, outsidelabhours):
    #Tell the system that the student is no longer in the lab
    student.atLab=False

    #load the last logged in time into memory
    lastLoggedIn=student.lastLoggedIn

    #Get the time now so we get the most accurate  time in relation to when they logged in
    timeNow=timezone.now()

    #Get the time they were in the lab and convert it from seconds to minutes
    minutesWorked=float((timeNow-lastLoggedIn).total_seconds())
    minutesWorked=minutesWorked/60
    if(save):
        hoursWorked = round(minutesWorked/60, 3)
    else:
        hoursWorked=0.0
    now = datetime.now()
    #Create the "Time worked" object to be added to the student database
    weights = 0
    hourspct = 0
    if not outsidelabhours:
        weights = LabHours.objects.filter(used = False).order_by("starttime").first().totalTime
        hourspct = (hoursWorked / weights) * 100
        if hourspct > 100:
            hourspct = 100
    timeWorked=HoursWorked(timeIn=lastLoggedIn,day = now.strftime("%A"),timeOut=timeNow, totalTime=hoursWorked, autoLogout=autolog, outsideLabHours = outsidelabhours, weight = weights, percentTime = hourspct)
    timeWorked.save()

    #add the time worked object to the student so it can be viewed in the calander
    student.hoursWorked.add(timeWorked)
    #add the minutes to the student's total time
    student.save()
    student.totalTime+= hoursWorked
    average, stddev = weighted_average_and_stddev(student)
    overallavg, overallstddev = student_overall_stats(student)
    totaldays, hahalol = get_total_days(student)
    percentdays = get_percent_days(student)
    mostday = most_frequent_day(student)
    student.mostFrequentDay = mostday
    student.percentDaysWorked = percentdays
    student.daysWorked = totaldays
    student.averageTime = overallavg
    student.stddevTime = overallstddev
    student.averagePercentTimeWeighted = average
    student.stddevPercentTimeWeighted = stddev
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

    try: 
        studentID=request.POST['studentID']
    except: 
        return render(request, 'attendanceapp/ScanCard.html')

    student=Student.objects.get(studentID=studentID)
    
    now = datetime.now()
    if student.atLab==True:
        if convertTime(LabHours.objects.filter(used = False).order_by("starttime").first().starttime) > now:
            minutes = logOut(student, True, False, True)
            timeReturn = str(math.trunc(minutes/60)) + " hours, " + " and " + str(math.trunc(minutes%60)) + " minutes"
            return render(request,'attendanceapp/ScanCard.html',{'message':"Hey " + student.name + "! You worked " + timeReturn + ", great job, it's not currently lab hours."})
        else:
            minutes = logOut(student, True, False, False)
            timeReturn = str(math.trunc(minutes/60)) + " hours, " + " and " + str(math.trunc(minutes%60)) + " minutes"
            return render(request,'attendanceapp/ScanCard.html',{'message':"Hey " + student.name + "! You worked " + timeReturn + ", great job!"})

    else:
        logIn(student)
        if convertTime(LabHours.objects.order_by("starttime").first().starttime) > now:
            return render(request,'attendanceapp/ScanCard.html',{'message':"Hey " + student.name + ", you just logged in. Good to see you outside lab hours"})
        else:
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
	
def viewPeopleInfo(request, chartID = "chart_ID", chart_type = "column", chart_height = 500):
	if request.method == "POST":
		form = SubteamForm(request.POST)
		if form.is_valid():
			print("haha lol")
	else:
		form = SubteamForm()
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
	
def leaderboard(request):
	table = StudentTable(Student.objects.order_by("-totalTime"))
	RequestConfig(request).configure(table)
	return render(request, "attendanceapp/leaderboard.html", {'students': table})
    
def viewPeopleStats(request):
    table = StatTable(Student.objects.filter(~Q(totalTime = 0)).order_by("-totalTime"))
    RequestConfig(request).configure(table)
    return render(request,"attendanceapp/viewPeopleStats.html",{"students":table})