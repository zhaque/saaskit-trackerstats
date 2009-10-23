from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'stats.views.index', name='stats_list'),
    url(r'^(?P<stats_id>\d+)/$', 'stats.views.index', name='tracker_list_stats_clicked'),
    url(r'^trend/(?P<trend_id>\d+)/$', 'stats.views.trend', name='stats_trend'),
    url(r'^pack/(?P<pack_id>\d+)/$', 'stats.views.pack', name='stats_pack'),
)
