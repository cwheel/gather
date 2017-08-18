import urllib2
import json

from utils import jsonPath

class PropertyAggregate(object):
    '''Represents a standard property aggregation'''

    def __init__(self, **kwargs):
        self.rootAggregates = []
        self.field = kwargs['field']
        self.url = kwargs['url']

        if 'keys' in kwargs: self.keys = kwargs['keys']
        if 'key' in kwargs: self.key = kwargs['key']

    def initilizeSubAggregates(self, json):
        pass

    def aggregate(self, **kwargs):
        url = self.url.format(kwargs['value'])

        response = urllib2.urlopen(url)
        resp = response.read()

        try:
            jsonResp = json.loads(resp)
        except:
            print 'Failed to parse {}, exiting aggregation branch!'.format(url)
            return

        if hasattr(self, 'key'):
            value = jsonPath.resolve(jsonResp, self.key)
            print 'Property resolved value: {}'.format(value)
        elif hasattr(self, 'keys'):
            for key in self.keys:
                value = jsonPath.resolve(jsonResp, key)
                print 'Property resolved: {}={}'.format(key,value)
