from django.conf.urls import patterns, url
from humster.views import view_semester, view_registers, view_stream, reload_stream

urlpatterns = patterns('',
    url(r'^semester/(?P<semester_id>\d+)$', view_semester, name='semester'),
    url(r'^stream/(?P<stream_id>\d+)$', view_stream, name='stream'),
    url(r'^stream/(?P<stream_id>\d+)/reload$', reload_stream, name='reload_stream'),

    url(r'^$', view_registers, name='registers')
)