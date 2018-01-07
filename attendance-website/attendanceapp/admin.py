from django.contrib import admin
from .models import Subteam, HoursWorked, Student, LabHours, OverallStats, UpdateAdmin, HoursWorkedAdmin

# Register your models here.

admin.site.register(Subteam, UpdateAdmin)
admin.site.register(HoursWorked, HoursWorkedAdmin)
admin.site.register(Student, UpdateAdmin)
admin.site.register(LabHours)
admin.site.register(OverallStats)