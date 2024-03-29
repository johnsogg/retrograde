from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'homework.views',
#    url(r'^$', 'index'),
    url(r'^course/(?P<course_id>\d+)/$', 'course'),
    url(r'^(?P<hw_id>\d+)/$', 'view_specific_assignment'),
    url(r'^(?P<hw_id>\d+)/submit/$', 'submit_homework'),
    url(r'^(?P<hw_id>\d+)/sub/(?P<sub_id>\d+)/$', 'view_specific_submission'),
    url(r'^course/(?P<course_id>\d+)/exam/(?P<exam_id>\d+)/', 'view_exam'),
)
