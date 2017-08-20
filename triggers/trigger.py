from threading import Thread

class Trigger(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.event = event

    def notify(self):
        self.event.set()
