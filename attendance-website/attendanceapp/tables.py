import django_tables2 as tables
from .models import Student, Subteam

class StudentTable(tables.Table):
    class Meta:
        model = Student
        exclude=("studentID", "id", "lastLoggedIn", "averageTime", "stddevTime", "percentDaysWorked", "averagePercentTimeWeighted", "stddevPercentTimeWeighted", "mostFrequentDay")
        per_page = "100"
        attrs = {"class": "paleblue"}
        
class StatTable(tables.Table):
    class Meta:
        model = Student
        exclude=("studentID", "id", "lastLoggedIn", "atLab")
        per_page = "100"
        attrs = {"class": "paleblue"}
        
class SubteamTable(tables.Table):
    class Meta:
        model = Subteam
        exclude=(["id"])
        per_page = "100"
        attrs = {"class": "paleblue"}