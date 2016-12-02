from __future__ import division
from attendanceapp.models import Student, LabHours
from datetime import datetime, timedelta
import operator
import numpy as np
import calendar
import math
import pytz

def check_data():
	data = {}
	sorteddata = {}
	names = []
	hours= []
	students = Student.objects.all()
	for student in students:
		names.append(str(student.name))
		hours.append(student.totalTime)
		data = zip(names, hours)
	sorteddata = zip(*sorted(data, key=operator.itemgetter(1), reverse=True))
	names = list(sorteddata[0])
	hours = list(sorteddata[1])
	return names, hours
    
def weighted_average_and_stddev(student):
    valuearr = np.array([])
    weightarr = np.array([])
    for hours in student.hoursWorked.all():
        valuearr = np.append(valuearr, hours.percentTime)
        weightarr = np.append(weightarr, hours.weight)
    try:
        average = np.average(valuearr, weights = weightarr)
        variance = np.average((valuearr - average)**2, weights = weightarr)
    except:
        average = 0
        variance = 0
    return(average, math.sqrt(variance))
    
def convertTime(time):
    timestamp = calendar.timegm(time.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert time.resolution >= timedelta(microseconds=1)
    realhours = local_dt.replace(microsecond=time.microsecond)
    return realhours
    
def most_common_in_list(inputlist):
    return max(set(inputlist), key=inputlist.count)
    
def most_common_day(student):
    strarr = []
    for hours in student.hoursWorked.all():
        strarr.append(hours.day)
    return most_common_in_list(strarr)
    
def utc_to_normal(utctime):
    timestamp = calendar.timegm(utctime.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert utctime.resolution >= timedelta(microseconds=1)
    realhours = local_dt.replace(microsecond=utctime.microsecond)
    return realhours
    
def student_overall_stats(student):
    hourarr = np.array([])
    for hours in student.hoursWorked.all():
        hourarr = np.append(hourarr, hours.totalTime)
    average = np.average(hourarr)
    stddev = np.std(hourarr)
    return average, stddev

def get_total_days(student):
    lastday = student.hoursWorked.first().timeIn
    totaldays = 1
    datearr = []
    for hours in student.hoursWorked.all():
        if hours.timeIn.date() != lastday.date() and hours.timeIn.date() != pytz.utc.localize(datetime.strptime('Jan 1 2000  12:00AM', '%b %d %Y %I:%M%p')):
            totaldays += 1
            datearr.append(hours.timeIn.date())
        lastday = hours.timeIn
    return totaldays, datearr
    
def get_percent_days(student):
    days, datearr = get_total_days(student)
    labdays = 0
    totallabdays = 0
    for labhours in LabHours.objects.all():
        for date in datearr:
            if labhours.starttime.date() == date:
                labdays = labdays + 1
        if labhours.starttime.date() <= datetime.now().date():
            totallabdays += 1
    percent = labdays/totallabdays
    percent *= 100
    return percent
    
def most_frequent_day(student):
    dayarr = []
    for hours in student.hoursWorked.all():
        dayarr.append(hours.day)
    filteredarr = filter(lambda a: a != "None", dayarr)
    try:
        day = max(set(filteredarr), key=filteredarr.count)
        return day
    except:
        return "None"