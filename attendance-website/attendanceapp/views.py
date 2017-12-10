from django.shortcuts import render
from attendanceapp.models import Subteam, HoursWorked, Student, LabHours, OverallStats
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from operator import itemgetter
from forms import SubteamForm
from attendanceapp.tables import StudentTable, StatTable, SubteamTable
from django_tables2 import RequestConfig
from datetime import datetime, timedelta
from pytz import timezone
from util import check_data, convertTime, weighted_average_and_stddev, student_overall_stats, get_total_days, get_percent_days, most_frequent_day, subteam_avg_and_stddev_pct, subteam_total_and_fqt_days, do_student_calcs

import math
import urllib2
import re
import logging
import pytz

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
    student.lastLoggedIn=datetime.now(tz=pytz.utc).astimezone(timezone('America/Los_Angeles'))

    #Write to the database
    student.save()


def logOut(student, save, autolog, outsidelabhours):
    #Tell the system that the student is no longer in the lab
    student.atLab=False

    #load the last logged in time into memory
    lastLoggedIn=student.lastLoggedIn

    #Get the time now so we get the most accurate  time in relation to when they logged in
    timeNow=datetime.now(tz=pytz.utc).astimezone(timezone('America/Los_Angeles'))

    #Get the time they were in the lab and convert it from seconds to minutes
    minutesWorked=float((timeNow-lastLoggedIn).total_seconds())
    minutesWorked=minutesWorked/60
    now = datetime.now()
    student.save()
    if(save):
        hoursWorked = round(minutesWorked/60, 3)
        #Create the "Time worked" object to be added to the student database
        weights = 0
        hourspct = 0
        if not outsidelabhours:
            try:
                weights = LabHours.objects.filter(used = False).order_by("starttime").first().totalTime
            except:
                weights = 0
            hourspct = (hoursWorked / weights) * 100
            if hourspct > 100:
                hourspct = 100
        timeWorked=HoursWorked(timeIn=lastLoggedIn,day = now.strftime("%A"),timeOut=timeNow, totalTime=hoursWorked, autoLogout=autolog, outsideLabHours = outsidelabhours, weight = weights, percentTime = hourspct)
        timeWorked.save()
        #add the time worked object to the student so it can be viewed in the calander
        student.hoursWorked.add(timeWorked)
        #add the minutes to the student's total time
        student.totalTime+= hoursWorked
        student.save()
        do_student_calcs(student)
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
        return render(request, "attendanceapp/ScanCard.html")
    
    try:
        student=Student.objects.get(studentID=studentID)
    except:
        return render(request, 'attendanceapp/ScanCard.html', {'message': "Student ID number not recognized. "})
    
    now = datetime.now()
    try:
        labtime = convertTime(LabHours.objects.filter(used = False).order_by("starttime").first().starttime)
    except:
        labtime = datetime.strptime('Jan 1 2020  12:00AM', '%b %d %Y %I:%M%p')
    if student.atLab==True:
        if labtime > now:
            minutes = logOut(student, True, False, True)
            timeReturn = str(math.trunc(minutes/60)) + " hours, " + " and " + str(math.trunc(minutes%60)) + " minutes"
            return render(request,'attendanceapp/ScanCard.html',{'message':"Hey " + student.name + "! You worked " + timeReturn + ", great job, it's not currently lab hours."})
        else:
            minutes = logOut(student, True, False, False)
            timeReturn = str(math.trunc(minutes/60)) + " hours, " + " and " + str(math.trunc(minutes%60)) + " minutes"
            return render(request,'attendanceapp/ScanCard.html',{'message':"Hey " + student.name + "! You worked " + timeReturn + ", great job!"})

    else:
        logIn(student)
        if labtime > now:
            return render(request,'attendanceapp/ScanCard.html',{'message':"Hey " + student.name + ", you just logged in. Good to see you outside lab hours"})
        else:
            return render(request,'attendanceapp/ScanCard.html',{'message':"Hey " + student.name + ", you just logged in. Good to see you!"})

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
	
def leaderboard(request):
	table = StudentTable(Student.objects.order_by("-totalTime"))
	RequestConfig(request).configure(table)
	return render(request, "attendanceapp/leaderboard.html", {'students': table})
    
def viewPeopleStats(request):
    table = StatTable(Student.objects.filter(~Q(totalTime = 0)).order_by("-totalTime"))
    RequestConfig(request).configure(table)
    return render(request,"attendanceapp/viewPeopleStats.html",{"students":table})
    
def viewSubteamStats(request):
    table = SubteamTable(Subteam.objects.all())
    RequestConfig(request).configure(table)
    return render(request,"attendanceapp/viewSubteamStats.html",{"subteams":table})