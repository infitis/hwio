#!/usr/bin/env python
#
# Copyright 2010 Infitis
# Author: Ruslan Keba <keba@infitis.dp.ua>
#

import sys
import logging
import signal
import time

from hwio.server.io import IOThread
from hwio.server.http import HttpServerThread

'''
hwio server
'''

__all__ = ('HwioServer',)

class HwioServer(object):
    
    DEFAULT_SETTINGS = {
        'debug': False,
        'http_port': 8040,
        'tick': 1.0,
    }
    
    def __init__(self, name, devices, signals, settings = None):
        self.name = name
        self.devices = devices
        self.signals = signals
        self.settings = HwioServer.DEFAULT_SETTINGS
        if type(settings) is dict:
            self.settings.update(settings)
        self.http_thread = None
        self.io_thread = None
        self.terminate = False
        
        # save global instance
        HwioServer._instance = self
        
        # logger
        self.log = logging.getLogger('HwioServer')
        self.log.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d [%(levelname)-09s] %(message)s', '%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)
    
    @classmethod
    def instance(cls):
        """Returns a global HwioServer instance."""
        
        if not hasattr(cls, "_instance"):
            raise ValueError('Global HwioServer instance is None')
        return cls._instance
    
    def start(self):
        
        # start all devices
        self.log.info('starting all devices...')
        for device in self.devices.values():
            self.log.debug('starting {0} device'.format(device.id))
            device.start()
        
        # catch SIGINT handler
        signal.signal(signal.SIGINT, sigint_handler)
        
        # start io reading thread
        self.log.info('starting io thread');
        self.start_io_thread()
        
        # start http server thread
        self.log.info('starting http server');
        self.start_http_server()
        
        self.wait_loop()
    
    
    def start_http_server(self):
        self.http_thread = HttpServerThread(self)
        self.http_thread.start()
    
    
    def start_io_thread(self):
        self.io_thread = IOThread(self)
        self.io_thread.start()
    
    
    def wait_loop(self):
        while True:
            if self.terminate:
                break
            else:
                time.sleep(1)
        
        self.shutdown()
        self.log.info('bye!')
    
    def shutdown(self):
        
        # shutdown http server
        self.log.debug('shutdown http server')
        self.http_thread.finish()
        self.http_thread.join()
        
        # shutdown io thread
        self.log.debug('shutdown io thread')
        self.io_thread.finish()
        self.io_thread.join()


def sigint_handler(signum, frame):
    HwioServer.instance().terminate = True

