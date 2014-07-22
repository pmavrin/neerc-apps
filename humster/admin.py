from django.contrib import admin
from humster.models import Student, Semester, Stream, Course

admin.site.register(Stream)
admin.site.register(Semester)
admin.site.register(Course)
admin.site.register(Student)

# Register your models here.
