#!/usr/bin/env python
#
# Copyright 2010 Infitis
# Author: Ruslan Keba <keba@infitis.dp.ua>
#

import json


'''
Base class of io signals
'''

__all__ = ('BaseSignal',)


class BaseSignal(object):
    
    def __init__(self, id, name, device, offset, bit, inverse=False, active=True, default=0):
        self.id = id
        self.name = name
        self.device = device
        self.offset = offset
        self.bit = bit
        self.inverse = inverse
        self.active = active
        self.default = default
        
        self.state = self.default
    
    
    def read(self):
        if not self.device:
            raise Exception('device is None')
        
        if self.active:
            self.state = self.device.read(self.offset, self.bit)
            if self.inverse:
                self.state = not self.state
        else:
            self.state = self.default
        
        return self.state
    
    
    def write(self, data):
        self.state = data
        
        if self.inverse:
            self.state = not self.state
        
        if not self.device:
            raise Exception('device is None')
        
        if self.active:
            self.device.write(self.offset, self.bit, self.state)
