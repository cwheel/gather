import urllib2
import json

from utils import resolve
from utils import jsonPath

class IndexAggregate(object):
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
        except BaseException as e:
            print 'Failed to parse {}, exiting aggregation branch!'.format(self.url)
            print e
            return

        indicies = jsonPath.resolve(jsonResp, self.key)

        for index in indicies:
            for aggregate in self.rootAggregates:
                print 'Processing index: {}'.format(index)
                aggregate.aggregate(value=index)
