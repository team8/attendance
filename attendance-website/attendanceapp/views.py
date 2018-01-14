from django.shortcuts import render
from attendanceapp.models import Subteam, HoursWorked, Student, LabHours, OverallStats
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from operator import itemgetter
from forms import SubteamForm
from attendanceapp.tables import StudentTable, StatTable, SubteamTable
from django_tables2 import RequestConfig
from datetime import datetime, timedelta, date
from util import check_data, convertTime, weighted_average_and_stddev, student_overall_stats, get_total_days, get_percent_days, most_frequent_day, subteam_avg_and_stddev_pct, subteam_total_and_fqt_days, do_student_calcs
from django.core.exceptions import PermissionDenied
from .adapter_slackclient import slack_events_adapter, SLACK_VERIFICATION_TOKEN
import threading

import math
import re
import json
import logging

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
    student.lastLoggedIn=datetime.now()

    #Write to the database
    student.save()


def logOut(student, save, autolog, outsidelabhours):
    #Tell the system that the student is no longer in the lab
    student.atLab=False

    #load the last logged in time into memory
    timeIn=student.lastLoggedIn

    #Get the time now so we get the most accurate  time in relation to when they logged in
    timeOut=datetime.now()
    
    timeWorked=HoursWorked(timeIn=timeIn,timeOut=timeOut,owner=student)
    timeWorked.save()
    
    if timeWorked.totalTime < 60.0:
    	timeWorked.autoLogout = True
    	timeWorked.save()
    
    #add the time worked object to the student so it can be viewed in the calander
    student.hoursWorked.add(timeWorked)
    #add the minutes to the student's total time
    student.save()
    
    return timeWorked.totalTime/60 #TODO: update with minutes worked


def makeNewStudent(ID):

    try:
        html = requests.post("https://palo-alto.edu/Forgot/Reset.cfm",data={"username":str(ID)}).text
        name = re.search(r'<input name="name" type="hidden" label="name" value="(.*?)"',html).group(1)
        Student(name=name,studentID=ID,subteam=Subteam.objects.get(name="Unknown")).save()
        return True
    except:
        return False

@login_required()    
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


# uncomment for the slackclient API client (https://github.com/slackapi/python-slackclient)
# from .adapter_slackclient import slack_events_adapter, SLACK_VERIFICATION_TOKEN
#----
# uncomment for the slacker API client (https://github.com/os/slacker)
# from .adapter_slacker import slack_events_adapter, SLACK_VERIFICATION_TOKEN
#----
# uncomment for a urllib2-based client implemented in client_urllib2.py
# This should work with Google App Engine.
# from .adapter_urllib2 import slack_events_adapter, SLACK_VERIFICATION_TOKEN


def render_json_response(request, data, status=None, support_jsonp=False):
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    callback = request.GET.get("callback")
    if not callback:
        callback = request.POST.get("callback")  # in case of POST and JSONP

    if callback and support_jsonp:
        json_str = "%s(%s)" % (callback, json_str)
        response = HttpResponse(json_str, content_type="application/javascript; charset=UTF-8", status=status)
    else:
        response = HttpResponse(json_str, content_type="application/json; charset=UTF-8", status=status)
    return response


@csrf_exempt
def slack_events(request, *args, **kwargs):  # cf. https://api.slack.com/events/url_verification
    # logging.info(request.method)
    if request.method == "GET":
        raise Http404("These are not the slackbots you're looking for.")

    try:
        # https://stackoverflow.com/questions/29780060/trying-to-parse-request-body-from-post-in-django
        event_data = json.loads(request.body.decode("utf-8"))
    except ValueError as e:  # https://stackoverflow.com/questions/4097461/python-valueerror-error-message
        logging.info("ValueError: "+str(e))
        return HttpResponse("")
    logging.info("event_data: "+str(event_data))

    # Echo the URL verification challenge code
    if "challenge" in event_data:
        return render_json_response(request, {
            "challenge": event_data["challenge"]
        })

    # Parse the Event payload and emit the event to the event listener
    if "event" in event_data:
        # Verify the request token
        request_token = event_data["token"]
        if request_token != SLACK_VERIFICATION_TOKEN:
            slack_events_adapter.emit('error', 'invalid verification token')
            message = "Request contains invalid Slack verification token: %s\n" \
                      "Slack adapter has: %s" % (request_token, SLACK_VERIFICATION_TOKEN)
            raise PermissionDenied(message)

        event_type = event_data["event"]["type"]
        logging.info("event_type: "+event_type)
        t = threading.Thread(target=slack_events_adapter.emit, args=(event_type, event_data))
        t.start()
        return HttpResponse("")

    # default case
    return HttpResponse("")
