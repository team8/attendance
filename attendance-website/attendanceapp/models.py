from django.db import models

# Create your models here.

class Subteam(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField()
    studentID = models.IntegerField()
    subteam = models.ForeignKey(Subteam)
