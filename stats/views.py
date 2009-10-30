from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect, HttpResponse
from tracker.models import Tracker, Trend, Pack, Channel, ParsedResult
from stats.models import BaseStatistics, Statistics, TrendStatistics, TrackerStatistics, PackStatistics, ChannelStatistics
from datetime import datetime, timedelta
from scratchpad.models import Scratchpad, Item
import gviz_api
import settings
from stats.search import SorlSearch
import simplejson

@login_required
def index(request, stats_id=None):
    context_vars = dict()
    trend_stats = list(TrendStatistics.objects.all())
    for ts in trend_stats[:]:
        if ts.trend.muaccount != request.muaccount:
            trend_stats.remove(ts)    
    context_vars['trend_stats'] = trend_stats
    
    if stats_id:
        context_vars['cur_stats'] = Statistics.objects.get(id=stats_id)
        context_vars['latest'] = context_vars['cur_stats'].owner.get_latest()
        if isinstance(context_vars['cur_stats'].owner, TrackerStatistics):
            tracker = context_vars['cur_stats'].owner.tracker
            context_vars['tracker'] = tracker

        google_desc = {
                       'interval': ('number', 'Interval'),
                       'daily_change': ('number', 'Daily change')}

        owner = context_vars['cur_stats'].owner
        google_data = []
        for stats in owner.stats.all():
            google_data.append({'interval':stats.interval, 'daily_change':float(stats.daily_change)})
        data_table = gviz_api.DataTable(google_desc)
        data_table.LoadData(google_data)
        context_vars['jscode'] = data_table.ToJSCode("jscode_data",
                               columns_order=("interval", "daily_change"),
                               order_by="interval")



        if request.method == 'POST':
            tracker = context_vars['cur_stats'].owner.get_tracker()
            try:
              spad = Scratchpad.objects.get(title=tracker.name, account=request.muaccount)
            except ObjectDoesNotExist:
                if request.muaccount.owner.quotas.scratchpad_nothing:
                    return HttpResponseRedirect(reverse('scratchpad-not-available'))
                create_tasks = False
                if request.muaccount.owner.quotas.scratchpad_full:
                    create_tasks = True
                spad = create_scratchpad(tracker.name, request.muaccount, request.user, create_tasks)
            item = Item()
            item.scratchpad = spad
            item.notes = 'Hello world'
            item.title = 'Saved results'
            item.author = request.user
            item.save()
            return HttpResponseRedirect(reverse('scratchpad-scratchpad_view',args=[spad.id]))

    return direct_to_template(request, template='stats.html', extra_context=context_vars)

@login_required
def trend(request, trend_id=None):
    context_vars = dict()
    trend_stats = list(TrendStatistics.objects.all())
    for ts in trend_stats[:]:
        if ts.trend.muaccount != request.muaccount:
            trend_stats.remove(ts)    
    context_vars['trend_stats'] = trend_stats
    
    if trend_id:
        trend_stat = TrendStatistics.objects.get(id=trend_id)
        context_vars['cur_trend'] = trend_stat
        tracker_stats = trend_stat.trackerstats.all()

        jscode = 'var data = new google.visualization.DataTable();\n'
        for tracker_stat in tracker_stats:
          jscode += 'data.addColumn("number", "%s");\n' % tracker_stat

        jscode += 'data.addRows(%d);\n' % BaseStatistics.STATS_LENGTH
        i=0
        j=0
        for tracker_stat in tracker_stats:
          for stats in tracker_stat.stats.all():
            jscode += 'data.setValue(%d, %d, %d);\n' % (j, i, stats.total_7days)
            j += 1
          i += 1
          j = 0
        context_vars['jscode'] = jscode

    return direct_to_template(request, template='stats.html', extra_context=context_vars)

@login_required
def tracker(request, tracker_id=None):
    context_vars = dict()
    trend_stats = list(TrendStatistics.objects.all())
    for ts in trend_stats[:]:
        if ts.trend.muaccount != request.muaccount:
            trend_stats.remove(ts)    
    context_vars['trend_stats'] = trend_stats
    
    if tracker_id:
        tracker_stat = TrackerStatistics.objects.get(id=tracker_id)
        context_vars['cur_tracker'] = tracker_stat

        jscode = 'var data = new google.visualization.DataTable();\n'
        jscode += 'data.addColumn("number", "%s");\n' % tracker_stat

        jscode += 'data.addRows(%d);\n' % BaseStatistics.STATS_LENGTH
        j=0
        for stats in tracker_stat.stats.all():
          jscode += 'data.setValue(%d, %d, %d);\n' % (j, 0, stats.total_7days)
          j += 1
        context_vars['jscode'] = jscode

    return direct_to_template(request, template='stats.html', extra_context=context_vars)

@login_required
def pack(request, pack_id=None):
    context_vars = dict()
    trend_stats = list(TrendStatistics.objects.all())
    for ts in trend_stats[:]:
        if ts.trend.muaccount != request.muaccount:
            trend_stats.remove(ts)    
    context_vars['trend_stats'] = trend_stats
    
    if pack_id:
        pack_stat = PackStatistics.objects.get(id=pack_id)
        context_vars['cur_pack'] = pack_stat
        channel_stats = pack_stat.channelstats.all()

        jscode = 'var data = new google.visualization.DataTable();\n'
        jscode += 'data.addColumn("string", "%s");\n' % 'Channel'
        jscode += 'data.addColumn("number", "%s");\n' % 'Mentions'

        jscode += 'data.addRows(%d);\n' % len(channel_stats)
        i=0
        for channel_stat in channel_stats:
          stat = channel_stat.stats.get(interval=24)
          jscode += 'data.setValue(%d, %d, "%s");\n' % (i, 0, channel_stat)
          jscode += 'data.setValue(%d, %d, %d);\n' % (i, 1, stat.total_7days)
          i += 1
        context_vars['jscode'] = jscode


    return direct_to_template(request, template='stats.html', extra_context=context_vars)

def channel(request, channel_id=None):
    context_vars = dict()
    trend_stats = list(TrendStatistics.objects.all())
    for ts in trend_stats[:]:
        if ts.trend.muaccount != request.muaccount:
            trend_stats.remove(ts)    
    context_vars['trend_stats'] = trend_stats
    
    if channel_id:
        channel_stat = ChannelStatistics.objects.get(id=channel_id)
        context_vars['cur_channel'] = channel_stat

        jscode = 'var data = new google.visualization.DataTable();\n'
        jscode += 'data.addColumn("number", "%s");\n' % channel_stat

        jscode += 'data.addRows(%d);\n' % BaseStatistics.STATS_LENGTH
        j=0
        for stats in channel_stat.stats.all():
          jscode += 'data.setValue(%d, %d, %d);\n' % (j, 0, stats.total_7days)
          j += 1
        context_vars['jscode'] = jscode

    return direct_to_template(request, template='stats.html', extra_context=context_vars)

def tracker_mentions_js(request, tracker_id):
    tracker = Tracker.objects.get(id=tracker_id)
    query = 'query:"%s"' % tracker.query
    filter_query = 'tracker:"%s"' % tracker.name
    return mentions_js(request, query, filter_query)
    
def mentions_js(request, query, filter_query=None):
    api = SorlSearch()
    api.init_options()
    res = api.fetch(query, filter_query)
    total_count = res['sorl']['numFound']
    total_res = res['sorl']['docs']
    res_count = len(total_res)
    while res_count < total_count:
        api.set_offset(res_count)
        res = api.fetch(query, filter_query)
        total_res += res['sorl']['docs']
        res_count = len(total_res)
    str = simplejson.dumps(total_res)
    str = 'var mentions = %s' % str
    return HttpResponse(str, mimetype="text/javascript")

def tracker_mentions_map(request, tracker_id):
    tracker = Tracker.objects.get(id=tracker_id)
    context = {'tracker': tracker}
    return mentions_map(request, context)

def mentions_map(request, context = {}):
    context['apikey'] = settings.GOOGLEAPI
    return direct_to_template(request, template='map.html', extra_context=context)


