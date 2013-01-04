from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'homework.views',
    url(r'^$', 'index'),
    url(r'^(?P<hw_id>\d+)/$', 'specific'),
)
