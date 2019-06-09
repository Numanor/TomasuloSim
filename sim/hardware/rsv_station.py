# -*- coding=utf-8 -*-
from sim.hardware.register import Reg


class RsvStation(object):
    
    def __init__(self, name):
        self.busy = False
        self.instr = None
        self.name = name

    def insert(self, instr):
        if self.busy:
            return False
        else:
            self.instr = instr
    
    def getStatus(self):
        return {
            'busy': ('Yes' if self.busy else 'No'),
            'name': self.name
        }

# RS for (OPR dstReg srcReg1 srcReg2) type instructions
class RR_Rsv(RsvStation):

    def __init__(self, name):
        RsvStation.__init__(self, name)
        self.Op = ''
        self.Vj = ''
        self.Vk = ''
        self.Qj = None
        self.Qk = None
    
    def getStatus(self):
        status = RsvStation.getStatus(self)
        status['op'] = self.Op
        status['vj'] = self.Vj
        status['vk'] = self.Vk
        status['qj'] = '' if self.Qj is None else self.Qj.name
        status['qk'] = '' if self.Qk is None else self.Qk.name
        return status
    
# Load Buffer
class LB_Rsv(RsvStation):

    def __init__(self, name):
        RsvStation.__init__(self, name)
        self.addr = ''

    def getStatus(self):
        status = RsvStation.getStatus(self)
        status['addr'] = self.addr