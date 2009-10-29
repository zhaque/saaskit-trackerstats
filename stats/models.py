from django.db import models
from datetime import datetime, timedelta
from tracker.models import Trend, Tracker, Pack, Channel, ParsedResult

# statistics is tree-like with trends as roots,
# trend1 - tracker1 - pack1 - channel1
#       \           \       \ channel2
#        \           \pack2 - channel1
#         \                 \ channel2
#          tracker2 - pack1 - channel1
#                   \       \ channel2
#                    \pack2 - channel1
#                           \ channel2

class BaseStatistics(models.Model):
    STATS_LENGTH = 7
    STATS_INTERVAL = 24
    created_date = models.DateTimeField('creation date', auto_now_add=True)

    def get_tracker(self):
        pass

    def get_startdate(self):
        pass

    def count_stats(self):
        self.stats.all().delete()
        now = datetime.now()
        for i in range (1, self.STATS_LENGTH+1):
            self.count_stats_with_interval(now, i * self.STATS_INTERVAL)

    def count_stats_with_interval(self, now, interval):
        stats = Statistics()
        stats.owner = self
        stats.interval = interval
        stats.save()

        date = now - timedelta(hours = interval)
        stats.daily_change = self.count_daily_change(date)
        stats.total_24hours = self.count_total_24hours(date)
        stats.total_7days = self.count_total_7days(date)
        stats.daily_average = self.count_daily_average(date)
        stats.save()

    def count_daily_change(self, date):
        today = self.count_total_24hours(date)
        yesterday = self.count_total_mentions(date-timedelta(days=2), date-timedelta(days=1))
        if 0 == yesterday:
            return None
        return '%s' % (float(today-yesterday)/yesterday*100)
        
    def count_daily_average(self, date):
        start = self.get_startdate()
        if start and start > date:
            return 0
        delta = (date - start).days + 1
        total = self.count_total_mentions(start, date)
        return total/delta
        
    def count_total_7days(self, date):
        return self.count_total_mentions(date - timedelta(days=7), date)

    def count_total_24hours(self, date):
        return self.count_total_mentions(date - timedelta(days=1), date)

    def count_total_mentions(self, startdate, finishdate):
        total = 0
        return total

    def get_latest(self):
        pass

class Statistics(models.Model):
    owner = models.ForeignKey(BaseStatistics, related_name='stats')
    interval = models.PositiveIntegerField()
    daily_change = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    total_24hours = models.PositiveIntegerField(blank=True, null=True)
    total_7days = models.PositiveIntegerField(blank=True, null=True)
    daily_average = models.IntegerField(blank=True, null=True)
    most_active_source = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('owner', 'interval')
    
    def __unicode__(self):
      return '%s' % self.owner

class TrendStatistics(BaseStatistics):
    trend = models.OneToOneField(Trend)

    class Meta:
        verbose_name = 'trend statistics'
        verbose_name_plural = 'trends statistics'

    def __unicode__(self):
        return '%s' % self.trend

    def get_startdate(self):
        startdates = []
        for tracker in self.trend.trackers.all():
            startdates.append(tracker.startdate)
        startdate = datetime.now()
        for date in startdates:
            if startdate > date:
                startdate = date
        return startdate

    def count_total_mentions(self, startdate, finishdate):
        total = 0
        for tracker in self.trend.trackers.all():
          for pack in tracker.packs.all():
            for channel in pack.channels.all():
              total += ParsedResult.objects.filter(query=tracker.query, channel=channel, date__range=(startdate, finishdate)).count()
        return total

    def get_latest(self):
        q_list = []
        for tracker in self.trend.trackers.all():
          channels = []
          for pack in tracker.packs.all():
              channels += list(pack.channels.all())
          q_list.append(Q(query=tracker.query, channel__in=channels))
        qs = Q()
        for q in q_list:
          qs = qs | q
        latest = ParsedResult.objects.filter(qs).order_by('-date')[:20]
        return latest

class TrackerStatistics(BaseStatistics):
    tracker = models.ForeignKey(Tracker, related_name='stats')
    trendstats = models.ForeignKey(TrendStatistics, related_name='trackerstats')

    class Meta:
        unique_together = ('tracker', 'trendstats')
        verbose_name = 'tracker statistics'
        verbose_name_plural = 'trackers statistics'

    def __unicode__(self):
        return '%s' % self.tracker

    def get_tracker(self):
        return self.tracker

    def get_startdate(self):
        return self.get_tracker().startdate

    def count_total_mentions(self, startdate, finishdate):
        total = 0
        for pack in self.tracker.packs.all():
          for channel in pack.channels.all():
            total += ParsedResult.objects.filter(query=self.tracker.query, channel=channel, date__range=(startdate, finishdate)).count()
        return total

    def get_latest(self):
        channels = []
        for pack in self.get_tracker().packs.all():
            channels += list(pack.channels.all())
        latest = ParsedResult.objects.filter(query=self.get_tracker().query, channel__in=channels).order_by('-date')[:20]
        return latest
        
class PackStatistics(BaseStatistics):
    pack = models.ForeignKey(Pack, related_name='stats')
    trackerstats = models.ForeignKey(TrackerStatistics, related_name='packstats')

    class Meta:
        unique_together = ('pack', 'trackerstats')
        verbose_name = 'pack statistics'
        verbose_name_plural = 'packs statistics'

    def __unicode__(self):
        return '%s' % self.pack

    def get_tracker(self):
        return self.trackerstats.tracker

    def get_startdate(self):
        return self.get_tracker().startdate

    def count_total_mentions(self, startdate, finishdate):
        total = 0
        for channel in self.pack.channels.all():
          total += ParsedResult.objects.filter(query=self.get_tracker().query, channel=channel, date__range=(startdate, finishdate)).count()
        return total

    def get_latest(self):
        channels = list(self.pack.channels.all())
        latest = ParsedResult.objects.filter(query=self.get_tracker().query, channel__in=channels).order_by('-date')[:20]
        return latest

class ChannelStatistics(BaseStatistics):
    channel = models.ForeignKey(Channel, related_name='stats')
    packstats = models.ForeignKey(PackStatistics, related_name='channelstats')

    class Meta:
        unique_together = ('channel', 'packstats')
        verbose_name = 'channel statistics'
        verbose_name_plural = 'channels statistics'

    def __unicode__(self):
        return '%s' % self.channel

    def get_tracker(self):
        return self.packstats.trackerstats.tracker

    def get_startdate(self):
        return self.get_tracker().startdate

    def count_total_mentions(self, startdate, finishdate):
        total = ParsedResult.objects.filter(query=self.get_tracker().query, channel=self.channel, date__range=(startdate, finishdate)).count()
        return total

    def get_latest(self):
        latest = ParsedResult.objects.filter(query=self.get_tracker().query, channel=self.channel).order_by('-date')[:20]
        return latest

