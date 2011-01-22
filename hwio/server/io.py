from threading import Thread
import time
import math


class IOThread(Thread):
    def __init__(self, hwio):
        Thread.__init__(self)
        self.hwio = hwio
        self.setName('hwio io thread')
        self.tick = hwio.settings['tick']
        self._finish = False
    
    def run(self):
        while True:
            now = time.time()
            interval = self.tick - (now - math.floor(now))
            time.sleep(interval)
            if self._finish:
                break
            self.hwio.log.debug('tick')
            # TODO: read signals
    
    def finish(self):
        self._finish = True

