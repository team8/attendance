from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def index(request):
    template = loader.get_template('attendanceapp/index.html')

    return HttpResponse(render(request, 'attendanceapp/index.html'))


def log_in(student):
    student.atLab = True
    student.lastLoggedIn = datetime.now()
    student.save()

# Create your views here.
