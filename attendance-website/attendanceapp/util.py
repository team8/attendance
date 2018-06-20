from __future__ import division
from datetime import datetime, timedelta, date
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
            hours.append(student.totalTime/3600.0)
            data = zip(names, hours)
    sorteddata = zip(*sorted(data, key=operator.itemgetter(1), reverse=True))
    names = list(sorteddata[0])
    hours = list(sorteddata[1])
    return names, hours
    



    
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

#fix
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

def total_hours(student):
    total = 0
    valid_total = 0
    for i in student.hoursWorked.all():
        total += i.totalTime
        valid_total += i.validTime
    student.totalTime = total
    student.validTime = valid_total

def do_student_calcs(student):

    total_hours(student)
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
            
def do_subteam_calcs(subteam):
    averageSub, stddevSub = subteam_avg_and_stddev_pct(subteam)

    subteam.averagePercentTimeWeighted = averageSub
    subteam.stddevPercentTimeWeighted = stddevSub

    totDays, mostFreqDay = subteam_total_and_fqt_days(subteam)
    subteam.totalDaysWorked = totDays
    subteam.mostFrequentDay = mostFreqDay

def subteam_avg_and_stddev_pct(team):
    #valuearr = np.array([])
    valuearr = np.array([])
    if valuearr.size != 0: 
        for student in Student.objects.filter(subteam=team): 
            valuearr = np.append(valuearr, student.averagePercentTimeWeighted)
    

    if valuearr.size != 0:
        average = np.average(valuearr)
        variance = np.average((valuearr - average)**2)
    else:
        average = 0
        variance = 0

    return (average, math.sqrt(variance))

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


def weighted_average_and_stddev(student):
    valuearr = np.array([])
    weightarr = np.array([])
    for hours in student.hoursWorked.all():
        if valuearr.size != 0 or weightarr.size != 0:
            valuearr = np.append(valuearr, hours.percentTime)
            weightarr = np.append(weightarr, hours.weight)

    #if valuearr.size != 0 or weightarr.size != 0:
        #average = np.average(valuearr, weights = weightarr)
        #variance = np.average((valuearr - average)**2, weights = weightarr)

    if valuearr.size != 0 or weightarr.size != 0:
        average = np.average(valuearr)
        variance = np.average((valuearr - average)**2)
    
    else:
        average = 0
        variance = 0
    return (average, math.sqrt(variance))

def do_hours_worked_calcs(timeWorked):

    timeOut=timeWorked.timeOut
    timeIn=timeWorked.timeIn
    
    timeWorked.day = timeOut.strftime("%A")
    
    #Move to hoursWorked model
    hours_elapsed = timeOut-timeIn
    timeWorked.totalTime = hours_elapsed.total_seconds()
    
    hours = LabHours.objects.all().filter(starttime__gt=datetime.combine(timeIn.date(), datetime.min.time()), starttime__lt=datetime.combine(timeIn.date(), datetime.min.time())+timedelta(days=1))
    time_deltas = []
    
    for i in hours:
    	
        if timeOut < i.starttime or timeIn > i.endtime:
            continue
        elif timeIn < i.starttime and timeOut > i.endtime:
            time_deltas.append(i.endtime - i.starttime)
        elif timeIn <= i.starttime and timeOut <= i.endtime:
            time_deltas.append(timeOut - i.starttime)
        elif timeIn >= i.starttime and timeOut >= i.endtime:
            time_deltas.append(i.endtime - timeIn)
        else:
            time_deltas.append(timeOut-timeIn)
            
    timeWorked.validTime = sum(time_deltas, timedelta()).total_seconds()
    try:
    	timeWorked.percentTime = float(timeWorked.validTime)/timeWorked.totalTime
    except:
    	timeWorked.percentTime = 0
    timeWorked.weight = sum((h.endtime-h.starttime).total_seconds() for h in hours)
    
from attendanceapp.models import Student, LabHours, Subteam