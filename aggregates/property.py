import urllib2
import json

from aggregate import Aggregate
from utils import jsonPath

class PropertyAggregate(Aggregate):
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
        url = self.url.format(kwargs['value'] or '')

        response = urllib2.urlopen(url)
        resp = response.read()

        try:
            jsonResp = json.loads(resp)
        except:
            print 'Failed to parse {}, exiting aggregation branch!'.format(url)
            return

        field = jsonPath.resolve(jsonResp, self.field)
        fields = []

        if hasattr(self, 'key'):
            value = jsonPath.resolve(jsonResp, self.key)

            if value is not None:
                fields.append({ 'field': self.__fieldName(field, self.key), 'value': value })
        elif hasattr(self, 'keys'):
            for key in self.keys:
                value = jsonPath.resolve(jsonResp, key)

                if value is not None:
                    fields.append({ 'field': self.__fieldName(field, key), 'value': value })

        return fields

    def __fieldName(self, field, key):
        safeField = ''.join(char for char in field[:1] + field.title()[1:] if not char.isspace())
        return '{}.{}'.format(safeField, key)
