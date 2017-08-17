from utils import resolve

class IndexAggregate(object):
    '''Represents an aggregation on an index, usually containing sub-aggregates'''

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            print 'Index with: {} = {}'.format(key, value)

        self.rootAggregates = []

    def initilizeSubAggregates(self, json):
        for rawAggregate in json:
            opts = rawAggregate.copy()
            opts.pop('aggregate', None)
            opts.pop('type', None)

            aggregate = resolve.aggregate(rawAggregate['type'], **opts)
            self.rootAggregates.append(aggregate)

            if 'aggregate' in rawAggregate:
                aggregate.initilizeSubAggregates(rawAggregate['aggregate'])

    def aggregate(self):
        pass
