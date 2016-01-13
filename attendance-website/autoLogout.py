from attendanceapp.models import Subteam, HoursWorked, Student
import time
import os

#This script is a modified version of our existing logOut function. It serves to auto log out all students who failed to do so manually, and gives them a set number of hours.
 logOut(student):
    studalse

    #Tell the system that the student is no longer in the lab
    lastastLoggedIn

    #This sets the amount of a time a student gets if they fail to log out manually in minutes
    minutesWorked 150

    #Create the "Time worked" object to be added to the student database
    timeWorked=HoursWorked(timeIn=lastLoggedIn,autoLogout=True, totalTime=minutesWorked)

    #Save the timeWorked object
    timeWorked.save()

    #Add the time worked object to the student so it can be viewed in the calender
    student.hoursWorked.add(timeWorked)

    #Add the minutes to the student's total time
    student.totalTime+=minutesWorked

    #Save the student object
    student.save()


    #Return the number of minutes spent in the lab
    return minutesWorked

#This the main that we're running on another thread in manage.py. Essentially, it runs constantly and checks whether or not it's 2am. If it is, it logs out all the students currently in the lab, using our modified logOut shown above.
def main():
    time.sleep(30) #Sleep for 30 seconds to allow models load into memory
    while True:
        try:
            if time.localtime().tm_hour == 2:
                Students = Student.objects.filter(atLab=True)
                for student in Students: logOut(student)

                time.sleep(82800)
            else: time.sleep(1800)
        except KeyboardInterrupt as e:
            break
