class PropertyAggregate(object):
    '''Represents a standard property aggregation'''

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            print 'Property with: {} = {}'.format(key, value)

        self.rootAggregates = []
        self.key = kwargs['key']
        self.field = kwargs['field']
        self.url = kwargs['url']

    def initilizeSubAggregates(self, json):
        pass

    def aggregate(self, **kwargs):
        pass
