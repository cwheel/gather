from utils import resolve
import connectors

class Pattern(object):
    '''A mapping of sources to fields'''

    def __init__(self, json, name):
        self.json = json
        self.rootAggregates = []
        self.name = name

        self.parsePattern()

    def parsePattern(self):
        rawAggregates = self.json['aggregate']
        rawConnection = self.json['save']['connection']
        connectorType = self.json['save']['type']

        for rawAggregate in rawAggregates:
            opts = rawAggregate.copy()
            opts.pop('aggregate', None)
            opts.pop('type', None)

            aggregate = resolve.aggregate(rawAggregate['type'], **opts)
            self.rootAggregates.append(aggregate)

            if 'aggregate' in rawAggregate:
                aggregate.initilizeSubAggregates(rawAggregate['aggregate'])

        self.connector = resolve.generic(connectors, connectorType, rawConnection, self.name)

    def run(self):
        aggregate = []

        for ag in self.rootAggregates:
            aggregate += ag.aggregate()

        self.connector.configureStore(aggregate)
        self.connector.createRecord(aggregate)

        return aggregate
