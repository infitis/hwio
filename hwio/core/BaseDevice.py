#!/usr/bin/env python
#
# Copyright 2010 Infitis
# Author: Ruslan Keba <keba@infitis.dp.ua>
#

'''
Base class of io devices
'''

__all__ = ('BaseDevice',)


class BaseDevice(object):
    
    def __init__(self, id, base_addr, irq=None, dma=None):
        self.model = 'unknown model'
        self.id = id
        self.base_addr = base_addr
        self.irq = irq
        self.dma = dma
    
    def start(self):
        ''' device starting operations '''
        pass
    
    def stop(self):
        ''' device stopping operations '''
        pass
    
    def read(self, offset, bit):
        ''' read data from hardware '''
        pass
    
    def write(self, offset, bit, data):
        ''' write data to hardware '''
        pass
    
    