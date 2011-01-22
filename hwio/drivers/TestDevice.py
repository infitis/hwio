#!/usr/bin/env python
#
# Copyright 2010 Infitis
# Author: Ruslan Keba <keba@infitis.dp.ua>
#

import random

from hwio.core.BaseDevice import BaseDevice
from hwio.core.BaseSignal import BaseSignal

'''
Device class which generate random signals for test purposes
'''

__all__ = ('TestDevice', 'TestSignal')

class TestDevice(BaseDevice):
    
    def __init__(self, id, base_addr, irq=None, dma=None):
        super(TestDevice, self).__init__(id, base_addr, irq, dma)
        self.model = 'Test Device'
    
    def read(self, offset, bit):
        return random.randint(0, 256)


class TestSignal(BaseSignal):
    
    def __init__(self, id, name, device, offset, bit, inverse=False, active=True, default=0):
        
        super(TestSignal, self).__init__(id, name, device, offset, bit, inverse, active, default)
        
        if self.device.__class__ != TestDevice:
            raise Exception('Test signal must be assigned to Test device')
