from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from tracker.models import Tracker, Trend, Pack, TrendStatistics, TrackerStatistics, PackStatistics, ChannelStatistics, Statistics, ParsedResult
from datetime import datetime, timedelta
from scratchpad.models import Scratchpad, Item

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
