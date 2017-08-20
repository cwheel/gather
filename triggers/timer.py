from time import sleep
from trigger import Trigger

class Timer(Trigger):
    '''Trigger which fires in response to time elapsing'''

    def __init__(self, event, **kwargs):
        super(Timer, self).__init__(event)

        self.every = kwargs['every']

    def run(self):
        self.__runLoop()

    def __runLoop(self):
        sleep(self.every)
        self.notify()

        self.__runLoop()
