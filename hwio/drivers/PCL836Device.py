#!/usr/bin/env python
#
# Copyright 2010 Infitis
# Author: Ruslan Keba <keba@infitis.dp.ua>
#

import os
import portio

from hwio.core.BaseDevice import BaseDevice

'''
Advantech PCL 836 devices classes
'''


__all__ = ('PCL836CountersDevice', 'PCL836DIODevice', 'MAX_COUNTER_VALUE')


# Counter control register format
CCR_EXTRENAL_CLOCK_WITHOUT_FILTER = 0x00
CCR_EXTERNAL_CLOCK_WITH_FILTER    = 0x01
CCR_INTERNAL_CLOCK                = 0x02
CCR_PWM                           = 0x03
CCR_POSITIVE_EDGE                 = 0x00
CCR_NEGATIVE_EDGE                 = 0x04

# Counter control register
SELECT_COUNTER_0                  = 0x00
SELECT_COUNTER_1                  = 0x40
SELECT_COUNTER_2                  = 0x80
SELECT_COUNTER_READ_BACK          = 0xc0

RW_COUNTER_LATCH                  = 0x00
RW_LSB                            = 0x10
RW_MSB                            = 0x20
RW_LSB_MSB                        = 0x30

MODE_0                            = 0x00
MODE_1                            = 0x02
MODE_2                            = 0x04
MODE_3                            = 0x06
MODE_4                            = 0x08
MODE_5                            = 0x0a

BCD_16_BIT                        = 0x00
BCD_DECIMAL                       = 0x01

MAX_COUNTER_VALUE                 = 0xffff

WR_RD_836                         = (0x40 & 0x7f)


class PCL836Device(BaseDevice):
    
    def __init__(self, id, base_addr, irq=None, dma=None):
        super(PCL836Device, self).__init__(id, base_addr, irq, dma)
        self.model = 'PCL836 Base Device'
    
    
    def start(self):
        
        status = portio.ioperm(self.base_addr, 24, 1)
        if status:
            raise Exception('ioperm: '+os.strerror(status))
        
        # todo: check device is connected


class PCL836CountersDevice(BaseDevice):
    
    def __init__(self, id, base_addr, irq=None, dma=None):
        super(PCL836CountersDevice, self).__init__(id, base_addr, irq, dma)
        self.model = 'PCL836 Counters'
    
    
    def start(self):
        
        super(PCL836CountersDevice, self).start()
        
        # set counters clock input mode
        self._set_counter_clock_input_mode(0,CCR_EXTRENAL_CLOCK_WITHOUT_FILTER | CCR_POSITIVE_EDGE)
        self._set_counter_clock_input_mode(1,CCR_EXTRENAL_CLOCK_WITHOUT_FILTER | CCR_POSITIVE_EDGE)
        self._set_counter_clock_input_mode(2,CCR_EXTRENAL_CLOCK_WITHOUT_FILTER | CCR_POSITIVE_EDGE)
        self._set_counter_clock_input_mode(3,CCR_EXTRENAL_CLOCK_WITHOUT_FILTER | CCR_POSITIVE_EDGE)
        self._set_counter_clock_input_mode(4,CCR_EXTRENAL_CLOCK_WITHOUT_FILTER | CCR_POSITIVE_EDGE)
        self._set_counter_clock_input_mode(5,CCR_EXTRENAL_CLOCK_WITHOUT_FILTER | CCR_POSITIVE_EDGE)
        
        # set counters
        self.write(0, 0, MAX_COUNTER_VALUE)
        self.write(1, 1, MAX_COUNTER_VALUE)
        self.write(2, 2, MAX_COUNTER_VALUE)
        self.write(3, 0, MAX_COUNTER_VALUE)
        self.write(4, 1, MAX_COUNTER_VALUE)
        self.write(5, 2, MAX_COUNTER_VALUE)
    
    
    def read(self, offset, bit):
        select=0
        if bit == 0:
            select=SELECT_COUNTER_0
        elif bit == 1:
            select=SELECT_COUNTER_1
        elif bit == 2:
            select=SELECT_COUNTER_2
        
        self._write_counter_control_word(offset, select | RW_LSB_MSB | MODE_1 | BCD_16_BIT)
        
        chip = 0
        if offset >= 3:
            chip = 1
        low = portio.inb(base+8+offset+chip)
        hi  = portio.inb(base+8+offset+chip)
        
        self.write(offset, bit, MAX_COUNTER_VALUE)
        
        return low + (hi << 8)
    
    
    def write(self, offset, bit, data):
        select=0
        if bit == 0:
            select=SELECT_COUNTER_0
        elif bit == 1:
            select=SELECT_COUNTER_1
        elif bit == 2:
            select=SELECT_COUNTER_2
        
        self._write_counter_control_word(offset, select | RW_LSB_MSB | MODE_1 | BCD_16_BIT)
        
        chip = 0
        if (offset >= 3):
            chip = 1
        
        portio.outb(data, self.base_addr+8+offset+chip)
        portio.outb(data >> 8, self.base_addr+8+offset+chip)
    
    
    def _set_counter_clock_input_mode(self, counter, mode):
        portio.outb(mode, self.base_addr+18+counter);
    
    
    def _write_counter_control_word(self, counter, control_word):
        chip = 0;
        if counter >= 3:
            chip = 1
        portio.outb(control_word, self.base_addr+11+chip*4)
    
    
    def _write_fout_control_word(self, fout, control_word):
        chip = 0;
        if fout >= 3:
            chip = 1
        portio.outb(control_word, self.base_addr+3+chip*4);


class PCL836DIODevice(BaseDevice):
    
    def __init__(self, id, base_addr, irq=None, dma=None):
        super(PCL836DIODevice, self).__init__(id, base_addr, irq, dma)
        self.model = 'PCL836 DIO'
        # digital output channels state
        self.do_state = [0,0]
    
    
    def start(self):
        super(PCL836DIODevice, self).start()
    
    
    def read(self, offset, bit):
        b = portio.inb(self.base_addr+16+offset)
        if bit < 0:
            return 0x00ff & b
        
        b = b << (7 - bit)
        b = b & 0x00ff
        b = b >> 7
        
        return b
    
    
    def write(self, offset, bit, data):
        
        channel = 0
        if offset == 1:
            channel = 1
        elif offset != 0:
            raise Exception('offset in out of bounds')
        
        if bit < 0:
            # out whole byte
            self.do_state[channel] = 0x00ff & data
            portio.outb(0x00ff & data, self.base_addr + 16 + channel)
        else:
            # out bit only
            
            mask = 0x01
            mask = mask << bit
            mask = mask & 0x00ff
            
            state = data << bit
            state = state & 0x00ff
            state = (state & mask) | (self.do_state[channel] & ~(mask))
            
            portio.outb(state, self.base_addr + 16 + channel)
            
            self.do_state[channel] = state
            
