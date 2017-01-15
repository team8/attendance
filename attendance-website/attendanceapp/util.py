from __future__ import division
from attendanceapp.models import Student, LabHours, Subteam
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
        if student.totalTime != 0:
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
    if hourarr.size != 0:  
        average = np.average(hourarr)
        stddev = np.std(hourarr)
    else:
        average = 0
        stddev = 0
    return average, stddev

def get_total_days(student):
    if student.hoursWorked.first() is not None:
        lastday = student.hoursWorked.first().timeIn
        totaldays = 1
        datearr = [student.hoursWorked.first().timeIn.date()]
        for hours in student.hoursWorked.all():
            if hours.timeIn.date() != lastday.date() and hours.timeIn.date() != pytz.utc.localize(datetime.strptime('Jan 1 2000  12:00AM', '%b %d %Y %I:%M%p')).date():
                totaldays += 1
                if not hours.timeIn.date() in datearr:
                    datearr.append(hours.timeIn.date())
            lastday = hours.timeIn
        return totaldays, datearr
    else:
        return 0, []
    
def get_percent_days(student):
    days, datearr = get_total_days(student)
    labdays = 0
    totallabdays = 1 #1 because they dont get set to used until 11:55 pm
    labdayarr = []
    for labhours in LabHours.objects.all():
        if labhours.used:
            totallabdays += 1
        labdayarr.append(labhours.starttime.date())
    for date in datearr:
        if date in labdayarr:
            labdays = labdays + 1
    try:
        percent = labdays/totallabdays
    except:
        percent = 0
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
        
def subteam_avg_and_stddev_pct(team):
    valuearr = np.array([])
    for student in Student.objects.filter(subteam=team): 
        valuearr = np.append(valuearr, student.averagePercentTimeWeighted)
    average = np.average(valuearr)
    variance = np.average((valuearr - average)**2)
    return (average, math.sqrt(variance))
    
def subteam_total_and_fqt_days(team):
    days = 1
    prevday = datetime.now().date()
    dayarr = []
    for student in Student.objects.filter(subteam=team):
        if student.hoursWorked.first() is not None:
            prevday = student.hoursWorked.first().timeIn
            for hours in student.hoursWorked.all():
                if hours.timeIn.date() != prevday.date() and hours.timeIn.date() != pytz.utc.localize(datetime.strptime('Jan 1 2000  12:00AM', '%b %d %Y %I:%M%p')).date():
                    days = days + 1
                    dayarr.append(hours.day)
    filteredarr = filter(lambda a: a!= "None", dayarr)
    try:
        day = max(set(filteredarr), key=filteredarr.count)
        return days, day
    except:
        return days, "None"
        
def do_student_calcs(student):
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
    student.save()

    for subteam in Subteam.objects.all():
        subteam.averagePercentTimeWeighted, subteam.stddevPercentTimeWeighted = subteam_avg_and_stddev_pct(subteam)
        subteam.totalDaysWorked, subteam.mostFrequentDay = subteam_total_and_fqt_days(subteam)
        subteam.save()