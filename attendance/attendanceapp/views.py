import math
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader

from attendanceapp.models import Student, LabHours, WorkTime
from attendanceapp.util import convert_time

from attendanceapp.forms import LoginForm


def index(request):
    template = loader.get_template('attendanceapp/index.html')

    return HttpResponse(render(request, 'attendanceapp/index.html'))


def log_in(student):
    student.atLab = True
    student.lastLoggedIn = datetime.now()
    student.save()


def log_out(student):
    # Tell the system that the student is no longer in the lab
    student.atLab = False

    # load the last logged in time into memory
    time_in = student.lastLoggedIn

    # Get the time now so we get the most accurate  time in relation to when they logged in
    time_out = datetime.now()

    time_worked = WorkTime(timeIn=time_in, timeOut=time_out, owner=student)
    time_worked.save()

    if time_worked.totalTime < 60.0:
        time_worked.autoLogout = True
        time_worked.save()

    # add the time worked object to the student so it can be viewed in the calendar
    student.hoursWorked.add(time_worked)
    # add the minutes to the student's total time
    student.save()

    return time_worked.totalTime / 60  # TODO: update with minutes worked


def login(request):
    if not 'studentID' in request.session or request.session['studentID'] == None:
        if request.method == 'GET':
            return render(request, 'attendanceapp/login.html', {'form': LoginForm()})
        elif request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                student_id = form.cleaned_data['name']
                try:
                    student = Student.objects.get(studentID=student_id)
                except:
                    return render(request, 'attendanceapp/login.html', {'form': LoginForm()})
                request.session['studentID'] = form.cleaned_data['name']

    return HttpResponseRedirect(request.GET.get('next', '/'))


@login_required()
def log_in_page(request):
    # Check if we are passed the student ID -> check if it is first time loading the page
    # If this passes, that means a student is logging in/out
    # If this fails...???

    try:
        student_id = request.POST['studentID']
    except:
        return render(request, "attendanceapp/ScanCard.html")

    try:
        student = Student.objects.get(studentID=student_id)
    except:
        return render(request, 'attendanceapp/ScanCard.html', {'message': "Student ID number not recognized. "})

    now = datetime.now()
    try:
        labtime = convert_time(LabHours.objects.filter(used=False).order_by("starttime").first().starttime)
    except:
        labtime = datetime.strptime('Jan 1 2020	 12:00AM', '%b %d %Y %I:%M%p')
    if student.atLab == True:
        if labtime > now:
            minutes = log_out(student, True, False, True)
            timeReturn = str(math.trunc(minutes / 60)) + " hours, " + " and " + str(
                math.trunc(minutes % 60)) + " minutes"
            return render(request, 'attendanceapp/ScanCard.html', {
                'message': "Hey " + student.name + "! You worked " + timeReturn + ", great job, it's not currently lab hours."})
        else:
            minutes = log_out(student, True, False, False)
            timeReturn = str(math.trunc(minutes / 60)) + " hours, " + " and " + str(
                math.trunc(minutes % 60)) + " minutes"
            return render(request, 'attendanceapp/ScanCard.html',
                          {'message': "Hey " + student.name + "! You worked " + timeReturn + ", great job!"})

    else:
        log_in(student)
        if labtime > now:
            return render(request, 'attendanceapp/ScanCard.html', {
                'message': "Hey " + student.name + ", you just logged in. Good to see you outside lab hours"})
        else:
            return render(request, 'attendanceapp/ScanCard.html',
                          {'message': "Hey " + student.name + ", you just logged in. Good to see you!"})
