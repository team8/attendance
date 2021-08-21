import calendar
from datetime import datetime, timedelta, date
from attendanceapp.models import *
import numpy as np
import math
import pytz


def most_common_in_list(inputlist):
    return max(set(inputlist), key=inputlist.count)


def most_common_day(student):
    strarr = []
    for hours in student.hoursWorked.all():
        strarr.append(hours.day)
    return most_common_in_list(strarr)


def convert_time(time):
    timestamp = calendar.timegm(time.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert time.resolution >= timedelta(microseconds=1)
    real_hours = local_dt.replace(microsecond=time.microsecond)
    return real_hours


def get_total_days(student):
    if student.hoursWorked.first() is not None:
        lastday = student.hoursWorked.first().timeIn
        totaldays = 1
        datearr = [student.hoursWorked.first().timeIn.date()]
        for hours in student.hoursWorked.all():
            if hours.timeIn.date() != lastday.date() and hours.timeIn.date() != pytz.utc.localize(
                    datetime.strptime('Jan 1 2000  12:00AM', '%b %d %Y %I:%M%p')).date():
                totaldays += 1
                if not hours.timeIn.date() in datearr:
                    datearr.append(hours.timeIn.date())
            lastday = hours.timeIn
        return totaldays, datearr
    else:
        return 0, []


# fix
def get_percent_days(student):
    days, datearr = get_total_days(student)
    labdays = 0
    totallabdays = 1  # 1 because they dont get set to used until 11:55 pm
    labdayarr = []
    for labhours in LabHours.objects.all():
        if labhours.used:
            totallabdays += 1
        labdayarr.append(labhours.startTime.date())
    for date in datearr:
        if date in labdayarr:
            labdays = labdays + 1
    try:
        percent = labdays / totallabdays
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
                if hours.timeIn.date() != prevday.date() and hours.timeIn.date() != pytz.utc.localize(
                        datetime.strptime('Jan 1 2000  12:00AM', '%b %d %Y %I:%M%p')).date():
                    days = days + 1
                    dayarr.append(hours.day)
    filteredarr = filter(lambda a: a != "None", dayarr)
    try:
        day = max(set(filteredarr), key=filteredarr.count)
        return days, day
    except:
        return days, "None"


def do_hours_worked_calcs(time_worked):
    time_out = time_worked.timeOut
    time_in = time_worked.timeIn

    time_worked.day = time_out.strftime("%A")

    # Move to hoursWorked model
    hours_elapsed = time_out - time_in
    time_worked.totalTime = hours_elapsed.total_seconds()

    hours = LabHours.objects.all().filter(startTime__gt=datetime.combine(time_in.date(), datetime.min.time()),
                                          startTime__lt=datetime.combine(time_in.date(),
                                                                         datetime.min.time()) + timedelta(days=1))
    time_deltas = []

    for i in hours:
        if time_out < i.startTime or time_in > i.endTime:
            continue
        elif time_in < i.startTime and time_out > i.endTime:
            time_deltas.append(i.endTime - i.startTime)
        elif time_in <= i.startTime and time_out <= i.endTime:
            time_deltas.append(time_out - i.startTime)
        elif time_in >= i.startTime and time_out >= i.endTime:
            time_deltas.append(i.endtime - time_in)
        else:
            time_deltas.append(time_out - time_in)

    time_worked.validTime = sum(time_deltas, timedelta()).total_seconds()
    try:
        time_worked.percentTime = float(time_worked.validTime) / time_worked.totalTime
    except:
        time_worked.percentTime = 0
    time_worked.weight = sum((h.endTime - h.startTime).total_seconds() for h in hours)


def total_hours(student):
    total = 0
    valid_total = 0
    for i in student.hoursWorked.all():
        total += i.totalTime
        valid_total += i.validTime
    student.totalTime = total
    student.validTime = valid_total


def weighted_average_and_stddev(student):
    valuearr = np.array([])
    weightarr = np.array([])
    for hours in student.hoursWorked.all():
        if valuearr.size != 0 or weightarr.size != 0:
            valuearr = np.append(valuearr, hours.percentTime)
            weightarr = np.append(weightarr, hours.weight)

    # if valuearr.size != 0 or weightarr.size != 0:
    # average = np.average(valuearr, weights = weightarr)
    # variance = np.average((valuearr - average)**2, weights = weightarr)

    if valuearr.size != 0 or weightarr.size != 0:
        average = np.average(valuearr)
        variance = np.average((valuearr - average) ** 2)

    else:
        average = 0
        variance = 0
    return average, math.sqrt(variance)


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
