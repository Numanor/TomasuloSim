# -*- coding=utf-8 -*-
from sim.hardware.rsv_station import RR_Rsv, LB_Rsv
from sim.hardware.func_unit import FU_Add, 
from sim.hardware.register import Reg

class Sched(object):

    def __init__(self, config):
        self.config = config
        self.ars = [RR_Rsv('Ars%d' % i) for i in range(0, config['ars'])
        self.mrs = [RR_Rsv('Mrs%d' % i) for i in range(0, config['mrs'])
        self.lb = [LB_Rsv('LB%d' % i) for i in range(0, config['lb'])
        self.add = [FU_Add('Add%d' % i) for i in range(0, config['add'])
        self.mul = [FU_Mult('Mult%d' % i) for i in range(0, config['mul'])
        self.ld = [FU_Load('Load%d' % i) for i in range(0, config['ld'])
        self.reg = [Reg('F%d' % i) for i in range(0, config['reg'])

    def isFinished(self):
        for i in self.ars:
            if i.busy:
                return False
        for i in self.mrs:
            if i.busy:
                return False
        for i in self.lb:
            if i.busy:
                return False
        return True
        

    def getStatus(self):
        status = {'rs':[], 'lb':[], 'reg':[]}
        for i in range(0, self.config['ars']):
            status['rs'].append(self.ars[i].getStatus())
        for i in range(0, self.config['mrs']):
            status['rs'].append(self.mrs[i].getStatus())
        for i in range(0, self.config['lb']):
            status['lb'].append(self.lb[i].getStatus())
        for i in range(0, self.config['reg']):
            status['reg'].append(self.reg[i].getStatus())
        

    def execCycle(self, instr):
        execRes = {'instr_status': {'issue':[], 'comp':[], 'wrtb':[]}}
        if instr is None:
            execRes['next_instr'] = -1
        return execRes
        