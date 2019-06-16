# -*- coding=utf-8 -*-
from typing import List, Text, Dict
from sim.NEL.parser import parse_instr
from sim.schedule.schedule import Sched

def runSim(config: Dict[Text, int], progFile: Text):
    with open(progFile, 'r') as f:
        codes = f.readlines()

    instrs = []
    instr_num = 0
    for line in codes:
        if line != '\n':
            instrs.append(parse_instr(line.strip('\n')))
            instrs[-1]['addr'] = instr_num
            instr_num += 1
        else:
            break
    instrs.append(None)
    
    sched = Sched(config)

    instr_status = [{'code':codes[i], 'issue':-1, 'comp':-1, 'wrtb':-1} for i in range(instr_num)]
    statusRecored = []
    next_instr = 0
    cycle = 1
    while instr_num > next_instr or not sched.isFinished():
        execRes = sched.execCycle(instrs[next_instr])
        next_instr = next_instr if execRes['next_instr'] is -1 else execRes['next_instr']
        for key in execRes['instr_status']:
            for _instr in execRes['instr_status'][key]:
                if instr_status[_instr][key] is -1:
                    instr_status[_instr][key] = cycle
        statusRecored.append(sched.getStatus())
        cycle += 1
    
    return (instr_status, statusRecored)

if __name__ == '__main__':
    a, b = runSim(config={
        'ars': 6,
        'mrs': 3,
        'lb': 3,
        'ld': 2,
        'add': 3,
        'mul': 2,
        'reg': 5
    }, progFile='./test.nel')
    print(a)
    print(b)