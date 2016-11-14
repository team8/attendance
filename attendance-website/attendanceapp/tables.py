import django_tables2 as tables
from .models import Student

class StudentTable(tables.Table):
	class Meta:
		model = Student
		#attrs = {"class": "name"}
		row_attrs = {"data-id": lambda record: record.pk}
		exclude=("lastLoggedIn", "atLab", "studentID", "id")
		per_page = "100"