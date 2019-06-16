# -*- coding=utf-8 -*-

class RsvStation(object):
    
    def __init__(self, name):
        self.busy = False
        self.instr = None
        self.name = name
        self.dst = None
        self.jump_imm = 0
        self.jump_dis = 0
        self.waitedby = []
        self.result = ''
    
    def getStatus(self):
        return {
            'busy': ('Yes' if self.busy else 'No'),
            'name': self.name
        }
    
    def clear(self):
        self.busy = False
        self.instr = None
        self.dst = None
        self.waitedby.clear()
        self.jump_int = ''
        self.jump_dis = ''

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

    def updateVal(self, src_rs):
        if self.Qj is src_rs:
            self.Qj = None
            self.Vj = src_rs.result
        if self.Qk is src_rs:
            self.Qk = None
            self.Vk = src_rs.result
        if self.Qj is None and self.Qk is None:
            return True
        return False

    def clear(self):
        RsvStation.clear(self)
        self.Op = ''
        self.Vj = ''
        self.Vk = ''
        self.Qj = None
        self.Qk = None
    
# Load Buffer
class LB_Rsv(RsvStation):

    def __init__(self, name):
        RsvStation.__init__(self, name)
        self.addr = ''

    def getStatus(self):
        status = RsvStation.getStatus(self)
        status['addr'] = self.addr
        return status

    def clear(self):
        RsvStation.clear(self)
        self.addr = ''