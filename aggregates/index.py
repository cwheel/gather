from utils.aggregateResolver import resolve

class IndexAggregate(object):
    '''Represents an aggregation on an index, usually containing sub-aggregates'''

    def __init__(self, **kwargs):
        self.rootAggregates = []

    def initilizeSubAggregates(self, json):
        rawAggregates = self.json['aggregate']

        for rawAggregate in rawAggregates:
            aggregate = resolve(self, rawAggregate['type'])
            self.rootAggregates.append(aggregate)

            if 'aggregate' in rawAggregate:
                aggregate.initilizeSubAggregates(rawAggregate['aggregate'])

    def aggregate(self):
        pass
