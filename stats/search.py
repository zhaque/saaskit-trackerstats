from livesearch.models import PipeSearch

#http://yonotes.com:8983/solr/select/?q=django&version=2.2&start=0&rows=10&indent=on&wt=json
#http://yonotes.com:8983/solr/select/?q=django&date:[NOW-7DAY%20TO%20NOW]&sort=date%20desc&version=2.2&start=0&rows=20&indent=on&wt=json
#createdate:[1995-12-31T23:59:59.999Z TO 2007-03-06T00:00:00Z]
#http://yonotes.com:8983/solr/select/?q=query:django%20channel:Twitter&version=2.2&start=0&rows=10&indent=on&wt=json
class SorlSearch(PipeSearch):
    uri = 'http://yonotes.com:8983/solr/select/'

    def init_options(self):
        super(SorlSearch, self).init_options()
        self.set_format()
        self.set_version()
        self.set_count()
        self.set_offset()
        self.set_sortby()

    def set_query(self, query):
        self.options.update({'q':query})

    def set_format(self, format='json'):
        self.options.update({'wt':format})

    def set_version(self, version='2.2'):
        self.options.update({'version':version})

    def set_count(self, count=20):
        self.options.update({'rows':count})

    def set_offset(self, offset=0):
        self.options.update({'start':offset})

    def set_sortby(self, sortby='date desc'):
        self.options.update({'sort':sortby})

    def set_range(self, q_range='date:[NOW-7DAYS TO NOW]'):
        self.options.update({'sort':q_range})

    def set_longitude(self, longitude):
        self.options.update({'longitude':longitude})

    def set_latitude(self, latitude):
        self.options.update({'latitude':latitude})

    def set_radius(self, radius):
        self.options.update({'radius':radius})

    def get_result(self, response):
        res = dict()
        if response and hasattr(response, "response"):
            res.update({'sorl':response.response,})

        return res
