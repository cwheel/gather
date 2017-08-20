import urllib2
import json

from aggregate import Aggregate
from utils import resolve
from utils import jsonPath

class Index(Aggregate):
    '''Represents an aggregation on an index, usually containing sub-aggregates'''

    def __init__(self, **kwargs):
        self.rootAggregates = []
        self.key = kwargs['key']
        self.url = kwargs['url']

    def initilizeSubAggregates(self, json):
        for rawAggregate in json:
            opts = rawAggregate.copy()
            opts.pop('aggregate', None)
            opts.pop('type', None)

            aggregate = resolve.aggregate(rawAggregate['type'], **opts)
            self.rootAggregates.append(aggregate)

            if 'aggregate' in rawAggregate:
                aggregate.initilizeSubAggregates(rawAggregate['aggregate'])

    def aggregate(self, **kwargs):
        response = urllib2.urlopen(self.url)
        resp = response.read()

        try:
            jsonResp = json.loads(resp)
        except:
            print 'Failed to parse {}, exiting aggregation branch!'.format(self.url)
            return

        indicies = jsonPath.resolve(jsonResp, self.key)

        fields = []

        for index in indicies:
            for aggregate in self.rootAggregates:
                results = aggregate.aggregate(value=index)

                if isinstance(results, list):
                    fields += results
                else:
                    fields.append(results)

        return fields
