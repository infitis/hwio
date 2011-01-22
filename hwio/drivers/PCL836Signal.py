#!/usr/bin/env python
#
# Copyright 2010 Infitis
# Author: Ruslan Keba <keba@infitis.dp.ua>
#

from hwio.core.BaseSignal import BaseSignal
from hwio.drivers.PCL836Device import PCL836CountersDevice, PCL836DIODevice, MAX_COUNTER_VALUE

'''
Base classes of PCL836 signals
'''

__all__ = ('PCL836CounterSignal', 'PCL836DIOSignal')


class PCL836CounterSignal(BaseSignal):
    
    def __init__(self, id, name, device, offset, bit, inverse=False, active=True, default=0):
        
        super(PCL836CounterSignal, self).__init__(id, name, device, offset, bit, inverse, active, default)
        
        if self.device.__class__ != PCL836CountersDevice:
            raise Exception('PCL836Counters signal must be assigned to PCL836Counters Device')
        
        self.prev_state = -1
    
    
    def read(self, offset, bit):
        if self.active:
            self.prev_state = self.state
            self.state = self.device.read(self.offset, self.bit)
            
            if self.prev_state == -1:
                
                self.prev_state = self.state
                self.state = self.default
            else:
                self.state = self.prev_state - self.state;
                if self.state < 0:
                    self.state += MAX_COUNTER_VALUE;
                #data = (int)(data / (core.io->tick1 / 1000.0));
        else:
            self.state = self.default
        
        return self.state


class PCL836DIOSignal(BaseSignal):
    
    def __init__(self, id, name, device, offset, bit, inverse=False, active=True, default=0):
        
        super(PCL836DIOSignal, self).__init__(id, name, device, offset, bit, inverse, active, default)
        
        if self.device.__class__ != PCL836DIODevice:
            raise Exception('PCL836DIO signal must be assigned to PCL836DIO Device')
            
    
    