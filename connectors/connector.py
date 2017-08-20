from abc import ABCMeta, abstractmethod

class Connector(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def configureStore(self, name, sample):
        pass

    @abstractmethod
    def createRecord(self):
        pass
