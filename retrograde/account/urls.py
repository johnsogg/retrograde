from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'account.views',
    url(r'^$', 'index'),
#    url(r'^(?P<hw_id>\d+)/$', 'specific'),
)
