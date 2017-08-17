from utils import resolve

class Pattern(object):
    '''A mapping of sources to fields'''

    def __init__(self, json):
        self.json = json
        self.rootAggregates = []
        self.parsePattern()

    def parsePattern(self):
        rawAggregates = self.json['aggregate']

        for rawAggregate in rawAggregates:
            opts = rawAggregate.copy()
            opts.pop('aggregate', None)
            opts.pop('type', None)

            aggregate = resolve.aggregate(rawAggregate['type'], **opts)
            self.rootAggregates.append(aggregate)

            if 'aggregate' in rawAggregate:
                aggregate.initilizeSubAggregates(rawAggregate['aggregate'])

    def run(self):
        pass
