from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader, RequestContext
from gspread.httpsession import HTTPError
from humster.googledoc import reload_stream_from_gd
from humster.models import Student, Stream, Semester


def view_registers(request):
    streams = Stream.objects.order_by('name')
    template = loader.get_template('registers.html')
    semesters = []
    for stream in streams:
        semesters.append(stream.semester_set.order_by('name'))
    context = RequestContext(request, {
        'streams': streams,
        'semesters_list': semesters,
    })
    return HttpResponse(template.render(context))


def view_semester(request, semester_id):
    semester = Semester.objects.get(pk=semester_id)
    template = loader.get_template('semester.html')
    courses = semester.course_set.order_by('name')
    students = semester.students.order_by('last_name')
    context = RequestContext(request, {
        'semester': semester,
        'courses': courses,
        'students': students
    })
    return HttpResponse(template.render(context))


def view_stream(request, stream_id, fail=None):
    stream = Stream.objects.get(pk=stream_id)
    template = loader.get_template('stream.html')
    context = RequestContext(request, {
        'stream': stream,
        'semesters': stream.semester_set.order_by('name'),
        'fail': fail,
    })
    return HttpResponse(template.render(context))


#controllers
def reload_stream(request, stream_id):
    stream = get_object_or_404(Stream, pk=stream_id)
    try:
        reload_stream_from_gd(stream)
    except HTTPError as e:
        return view_stream(request, stream_id, "ERROR: " + e.message)
        # return HttpResponseRedirect(reverse('stream_fail', args=(stream.id, e.message)))
        # return HttpResponseRedirect(reverse('registers'))

    return HttpResponseRedirect(reverse('stream', args=(stream.id,)))



