# -*- coding=utf-8 -*-
from 
from typing import Text, List

# class NELSyntaxError(Error):

#     def __init__(self, instruction, message):
#         self.instruction = instruction
#         self.message = message


def parse_add(params: List[Text]):
    
    pass

def parse_mul(params: List[Text]):
    pass

def parse_sub(params: List[Text]):
    pass

def parse_div(params: List[Text]):
    pass

def parse_ld(params: List[Text]):
    pass

def parse_jump(params: List[Text]):
    pass

# instruction type
parse_instr = {
    'ADD': parse_add,
    'SUB': parse_sub,
    'MUL': parse_mul,
    'DIV': parse_div,
    'LD': parse_ld,
    'JUMP': parse_jump
}



def parse_instr(line: Text):
    words = line.split(',')
    if words[0] not in parse_instr:
        print("UNKNOW instruction!", line)
        # raise NELSyntaxError(line, "UNKNOW instruction!")
    return parse_instr[words[0]](words[1:])

