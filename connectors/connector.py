from abc import ABCMeta, abstractmethod

class Connector(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def configureStore(self, name, aggregateResults):
        pass

    @abstractmethod
    def createRecord(self, aggregateResults):
        pass
