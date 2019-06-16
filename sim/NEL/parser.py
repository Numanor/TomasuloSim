# -*- coding=utf-8 -*-
from typing import Text, List

# class NELSyntaxError(Error):

#     def __init__(self, instruction, message):
#         self.instruction = instruction
#         self.message = message

def parse_param(params: List[Text]):
    res = {'params':[]}
    for param in params:
        if param[0] is 'F':
            res['params'].append(int(param[1:], base=10))
        else:
            res['params'].append(param)
    return res

# instruction type
opnum_instr = {
    'ADD': 4,
    'SUB': 4,
    'MUL': 4,
    'DIV': 4,
    'LD': 3,
    'JUMP': 4
}



def parse_instr(line: Text):
    words = line.split(',')
    # if words[0] in opnum_instr:
    #     if len(words[0]) != opnum_instr[words[0]]:
    #         print('opnum error!', line)
    # else:
    #     print('UNKNOW instruction!', line)
    ans = parse_param(words[1:])
    ans['op'] = words[0]
    return ans

