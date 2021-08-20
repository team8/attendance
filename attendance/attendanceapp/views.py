from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse(render(request, 'attendanceapp/index.html'))

# Create your views here.
