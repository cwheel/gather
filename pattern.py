from threading import Event

import triggers
import connectors

from utils import resolve

class Pattern(object):
    '''A detailed plan of the data to gather, how to store it, and when to aggregate it'''

    def __init__(self, json, name):
        self.json = json
        self.rootAggregates = []
        self.triggers = []
        self.name = name
        self.triggerEvent = Event()

        self.parsePattern()

    def parsePattern(self):
        rawAggregates = self.json['aggregate']
        rawConnection = self.json['save']['connection']
        rawTriggers = self.json['triggers']

        connectorType = self.json['save']['type']

        for rawAggregate in rawAggregates:
            opts = rawAggregate.copy()
            opts.pop('aggregate', None)
            opts.pop('type', None)

            aggregate = resolve.aggregate(rawAggregate['type'], **opts)
            self.rootAggregates.append(aggregate)

            if 'aggregate' in rawAggregate:
                aggregate.initilizeSubAggregates(rawAggregate['aggregate'])

        for rawTrigger in rawTriggers:
            opts = rawTrigger.copy()
            opts.pop('type', None)

            trigger = resolve.generic(triggers, rawTrigger['type'], self.triggerEvent, **opts)
            self.triggers.append(trigger)

        self.connector = resolve.generic(connectors, connectorType, rawConnection, self.name)

    def run(self):
        self.connector.configureStore(self.__aggregate())

        for trigger in self.triggers:
            trigger.start()

        self.__runLoop()

    def __runLoop(self):
        self.triggerEvent.wait()
        self.triggerEvent.clear()

        self.connector.createRecord(self.__aggregate())

        self.__runLoop()

    def __aggregate(self):
        results = []

        for ag in self.rootAggregates:
            results += ag.aggregate()

        return results
