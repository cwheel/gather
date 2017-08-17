class PropertyAggregate(object):
    '''Represents a standard property aggregation'''

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            print 'Property with: {} = {}'.format(key, value)

        self.rootAggregates = []

    def initilizeSubAggregates(self, json):
        pass

    def aggregate(self):
        pass
