test:
	 python -m py_compile attendance-website/manage.py
	 python -m py_compile attendance-website/attendance/urls.py
	 python -m py_compile attendance-website/attendance/wsgi.py
	 python -m py_compile attendance-website/attendance/settings.py
	 python -m py_compile attendance-website/attendanceapp/admin.py
	 python -m py_compile attendance-website/attendanceapp/models.py
	 python -m py_compile attendance-website/attendanceapp/tests.py
	 python -m py_compile attendance-website/attendanceapp/views.py
	 python -m py_compile attendance-website/attendanceapp/management/commands/logout.py
	 python -m py_compile attendance-website/attendanceapp/forms.py
	 python -m py_compile attendance-website/attendanceapp/tables.py
	 python -m py_compile attendance-website/attendanceapp/views.py
	 python -m py_compile attendance-website/attendanceapp/util.py
	 python -m py_compile attendance-website/attendanceapp/management/commands/synchours.py
	 python -m py_compile attendance-website/attendanceapp/management/commands/clearhours.py