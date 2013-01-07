from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'account.views',
    url(r'^$', 'index'),
    url(r'^create$', 'create'),
    url(r'^logout$', 'log_out'),
#    url(r'^(?P<hw_id>\d+)/$', 'specific'),
)
