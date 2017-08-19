from abc import ABCMeta, abstractmethod

class Aggregate(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def initilizeSubAggregates(self, json):
        pass

    @abstractmethod
    def aggregate(self, **kwargs):
        pass
