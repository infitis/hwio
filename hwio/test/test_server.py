#!/usr/bin/env python
#
# Copyright 2010 Infitis
# Author: Ruslan Keba <keba@infitis.dp.ua>
#

'''
test hwio server
'''

from hwio.server import HwioServer
from hwio.drivers.TestDevice import TestDevice, TestSignal
from hwio.drivers.PCL836Device import PCL836CountersDevice, PCL836DIODevice
from hwio.drivers.PCL836Signal import PCL836CounterSignal, PCL836DIOSignal

def main():
    devices = {
        'devtest'        : TestDevice('devtest', 0x100),
        #'pcl836counters' : PCL836CountersDevice('pcl836counters', 0x200),
        #'pcl836dio'      : PCL836CountersDevice('pcl836dio', 0x300),
    }
    
    signals = {
        'ts0' : TestSignal('ts0', 'test signal 0', devices['devtest'], 0, 0),
        'ts1' : TestSignal('ts1', 'test signal 1', devices['devtest'], 0, 1),
    }
    
    settings = {
        'http_port' : 8040,
        'debug' : True,
        'tick': 2.0,
    }
    
    server = HwioServer('TEST SERVER', devices, signals, settings)
    server.start()


if __name__=="__main__":
    main()