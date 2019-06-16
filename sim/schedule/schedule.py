# -*- coding=utf-8 -*-
from sim.hardware.rsv_station import RR_Rsv, LB_Rsv, RsvStation
from sim.hardware.func_unit import FU_Add, FU_Mult, FU_Load
from sim.hardware.register import Reg
from sim.utils.hexint import hex2int, int2hex

INSTR_USES_ADD = ['ADD', 'JUMP', 'SUB']
INSTR_USES_LD = ['LD']
INSTR_USES_MUL = ['MUL', 'DIV']

class Sched(object):

    def __init__(self, config):
        self.config = config
        self.ars = [RR_Rsv('Ars%d' % i) for i in range(1, config['ars']+1)]
        self.mrs = [RR_Rsv('Mrs%d' % i) for i in range(1, config['mrs']+1)]
        self.lb = [LB_Rsv('LB%d' % i) for i in range(1, config['lb']+1)]
        self.add = [FU_Add('Add%d' % i) for i in range(1, config['add']+1)]
        self.mul = [FU_Mult('Mult%d' % i) for i in range(1, config['mul']+1)]
        self.ld = [FU_Load('Load%d' % i) for i in range(1, config['ld']+1)]
        self.reg = [Reg('F%d' % i) for i in range(0, config['reg'])]
        self.writeback = []
        self.readyexec = []
        self.stalled = False

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
        return status

    def insertInstr(self, instr, issuedTo):
        issuedTo.instr = instr
        issuedTo.busy = True
        issuedTo.Op = instr['op']
        if issuedTo.Op == 'JUMP':
            issuedTo.jump_imm = hex2int(instr['params'][0])
            issuedTo.jump_dis = hex2int(instr['params'][2])
            reg = self.reg[instr['params'][1]]
            if reg.state is None:
                issuedTo.Vj = reg.val
            else:
                issuedTo.Qj = reg.state
                reg.state.waitedby.append(issuedTo)
        else:
            if isinstance(instr['params'][1], str):
                issuedTo.Vj = instr['params'][1]
            else:
                reg = self.reg[instr['params'][1]]
                if reg.state is None:
                    issuedTo.Vj = reg.val
                else:
                    issuedTo.Qj = reg.state
                    reg.state.waitedby.append(issuedTo)
            if isinstance(instr['params'][2], str):
                issuedTo.Vk = instr['params'][2]
            else:
                reg = self.reg[instr['params'][2]]
                if reg.state is None:
                    issuedTo.Vk = reg.val
                else:
                    issuedTo.Qk = reg.state
                    if reg.state != issuedTo.Qj:
                        reg.state.waitedby.append(issuedTo)
            issuedTo.dst = self.reg[instr['params'][0]]
            issuedTo.dst.state = issuedTo
        if issuedTo.Qj is None and issuedTo.Qk is None:
            return True
        return False

    def insertInstr_LD(self, instr, issuedTo):
        issuedTo.instr = instr
        issuedTo.busy = True
        issuedTo.addr = instr['params'][1]
        issuedTo.dst = self.reg[instr['params'][0]]
        issuedTo.dst.state = issuedTo

    def execCycle(self, instr):
        # print('come in', instr)
        execRes = {'instr_status': {'issue':[], 'comp':[], 'wrtb':[]}}
            
        # 1. WriteBack
        for rs in self.writeback:
            # 1.1 check if need write back
            # print('writeback', rs)
            if rs.dst is not None: # for 'JUMP', dst = None
                if rs.dst.state is rs:
                    rs.dst.val = rs.result
                    rs.dst.state = None
                for _rs in rs.waitedby:
                    if _rs.updateVal(rs):
                        self.readyexec.append(_rs)
            execRes['instr_status']['wrtb'].append(rs.instr['addr'])
            # 1.2 clear up reserve station
            rs.clear()
        self.writeback.clear()
        
        # 2. Issue (if any rs available)
        if instr is None or self.stalled:
            # if there is no instr left OR stalled by jump
            # no instructions will be issued
            execRes['next_instr'] = -1
        else:
            issuedTo = None
            if instr['op'] in INSTR_USES_ADD:
                for _rs in self.ars:
                    if not _rs.busy:
                        issuedTo = _rs
                        if self.insertInstr(instr, issuedTo):
                            self.readyexec.append(issuedTo)
                        break
            elif instr['op'] in INSTR_USES_MUL:
                for _rs in self.mrs:
                    if not _rs.busy:
                        issuedTo = _rs
                        if self.insertInstr(instr, issuedTo):
                            self.readyexec.append(issuedTo)
                        break
            else:
                for _rs in self.lb:
                    if not _rs.busy:
                        issuedTo = _rs
                        self.insertInstr_LD(instr, issuedTo)
                        self.readyexec.append(issuedTo)
                        break
                        
            if issuedTo is None:
                execRes['next_instr'] = instr['addr']
            else:
                execRes['instr_status']['issue'].append(instr['addr'])
                execRes['next_instr'] = instr['addr'] + 1
                if instr['op'] == 'JUMP':
                    self.stalled = True

        # 3. Exec FU
        for unit in self.add:
            if unit.remain > 0:
                unit.remain -= 1
                if unit.remain == 0:
                    self.writeback.append(unit.rs)
                    if unit.rs.Op == 'JUMP':
                        self.stalled = False
                        if hex2int(unit.rs.result) == unit.rs.jump_imm:
                            # print(unit.rs.jump_dis)
                            # print(unit.rs.result, unit.rs.jump_imm)
                            execRes['next_instr'] = unit.rs.instr['addr'] + unit.rs.jump_dis
                        else:
                            execRes['next_instr'] = unit.rs.instr['addr'] + 1
                    execRes['instr_status']['comp'].append(unit.rs.instr['addr'])
                    unit.clear()
        for unit in self.mul:
            if unit.remain > 0:
                unit.remain -= 1
                if unit.remain == 0:
                    self.writeback.append(unit.rs)
                    execRes['instr_status']['comp'].append(unit.rs.instr['addr'])
                    unit.clear()
        for unit in self.ld:
            if unit.remain > 0:
                unit.remain -= 1
                if unit.remain == 0:
                    self.writeback.append(unit.rs)
                    execRes['instr_status']['comp'].append(unit.rs.instr['addr'])
                    unit.clear()

        # 4. Pick & Exec
        self.readyexec.sort(key=lambda RsvStation: RsvStation.instr['addr'])
        # for i in self.readyexec:
            # print('ready:', i.instr)
        picked = []
        for _rs in self.readyexec:
            if _rs.instr['op'] in INSTR_USES_ADD:
                for i in self.add:
                    if i.rs is None:
                        picked.append(_rs)
                        i.rs = _rs
                        if _rs.instr['op'] == 'ADD':
                            i.remain = 3
                            _rs.result = int2hex(int(hex2int(_rs.Vj) + hex2int(_rs.Vk)))
                        elif _rs.instr['op'] == 'SUB':
                            i.remain = 3
                            _rs.result = int2hex(int(hex2int(_rs.Vj) - hex2int(_rs.Vk)))
                        else:
                            i.remain = 1
                            _rs.result = _rs.Vj
                        break
            elif _rs.instr['op'] in INSTR_USES_MUL:
                for i in self.mul:
                    if i.rs is None:
                        picked.append(_rs)
                        i.rs = _rs
                        if _rs.instr['op'] == 'MUL':
                            i.remain = 12
                            _rs.result = int2hex(int(hex2int(_rs.Vj) * hex2int(_rs.Vk)))
                        else:
                            if hex2int(_rs.Vk) == 0: # divided by 0
                                i.remain = 1
                                _rs.result = int2hex(hex2int(_rs.Vj))
                            else:
                                i.remain = 40
                                _rs.result = int2hex(int(hex2int(_rs.Vj)/hex2int(_rs.Vk)))
                        break
            else:
                for i in self.ld:
                    if i.rs is None:
                        picked.append(_rs)
                        i.rs = _rs
                        i.remain = 3
                        _rs.result = _rs.addr
                        break
        tmp = []
        for i in self.readyexec:
            if i not in picked:
                tmp.append(i)
        self.readyexec = tmp
        return execRes
        