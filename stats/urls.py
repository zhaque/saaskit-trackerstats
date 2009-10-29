from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'stats.views.index', name='stats_list'),
    url(r'^trend/(?P<trend_id>\d+)/$', 'stats.views.trend', name='stats_trend'),
    url(r'^tracker/(?P<tracker_id>\d+)/$', 'stats.views.tracker', name='stats_tracker'),
    url(r'^pack/(?P<pack_id>\d+)/$', 'stats.views.pack', name='stats_pack'),
    url(r'^channel/(?P<channel_id>\d+)/$', 'stats.views.channel', name='stats_channel'),
    url(r'^mentions/json/$', 'stats.views.mentions_json', name='stats_mentions_json'),
    url(r'^mentions/map/$', 'stats.views.mentions_map', name='stats_mentions_map'),
)
