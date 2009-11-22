from stats.models import TrendStatistics, TrackerStatistics, PackStatistics, ChannelStatistics, Statistics
from django.contrib import admin

class StatisticsInline(admin.TabularInline):
    model = Statistics

class TrendStatisticsAdmin(admin.ModelAdmin):
    pass
#    inlines = [StatisticsInline,]

admin.site.register(TrendStatistics, TrendStatisticsAdmin)
admin.site.register(TrackerStatistics)
admin.site.register(PackStatistics)
admin.site.register(ChannelStatistics)

