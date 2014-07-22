from django.db import models
import math


class State:
    PENDING = 0
    OK = 1
    ERROR = 2
    DISABLED = 3
    CHOICE = (
        (0, "pending"),
        (1, "ok"),
        (2, "error"),
        (3, "disabled")
    )


class Stream(models.Model):
    name = models.CharField(max_length=100, default="?")
    gd_spreadsheet_name = models.CharField(max_length=100, default="?")
    synced_with_spreadsheed = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=100, default="?")
    last_name = models.CharField(max_length=100, default="?")
    father_name = models.CharField(max_length=100, default="?")
    group = models.IntegerField(default=0)
    stream = models.ForeignKey(Stream)
    state = models.IntegerField(default=State.PENDING, choices=State.CHOICE)

    def full_name(self):
        return self.last_name + " " + self.first_name + " " + self.father_name

    def __str__(self):
        return self.first_name + " " + self.last_name


class Semester(models.Model):
    name = models.CharField(max_length=100, default="?")
    gd_sheet_name = models.CharField(max_length=100, default="?")
    stream = models.ForeignKey(Stream)
    year = models.CharField(max_length=10, default="?")
    semester_num = models.IntegerField(default=0)
    ordering = ['name']
    state = models.IntegerField(default=State.PENDING, choices=State.CHOICE)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.stream.name + " - " + self.name


class Course(models.Model):
    name = models.CharField(max_length=100, default="?")
    official_name = models.CharField(max_length=100, default="?")
    semester = models.ForeignKey(Semester)
    update_mode = models.CharField(max_length=20, default="?")
    state = models.IntegerField(default=State.PENDING, choices=State.CHOICE)

    def __str__(self):
        return self.name


class Score(models.Model):
    person = models.ForeignKey(Student)
    course = models.ForeignKey(Course)
    score = models.IntegerField(default=-1)
    state = models.IntegerField(default=State.PENDING, choices=State.CHOICE)
    log = models.CharField(max_length=1000)

def parse_score(s):
    s = s.strip()
    if len(s) == 0:
        return -1
    elif s[0].isdigit():
        try:
            return math.floor(float(s))
        except ValueError:
            return -1
    e







