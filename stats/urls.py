from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'stats.views.index', name='stats_list'),
    url(r'^(?P<stats_id>\d+)/$', 'stats.views.index', name='tracker_list_stats_clicked'),
)
