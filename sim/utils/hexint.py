# -*- coding=utf-8 -*-
from typing import Text

MAX_POS = 2**31-1
MAX_UNSIGNED = 2**32
width = 32

def hex2int(hex: Text):
    res = int(hex, 16)
    if res > MAX_POS:
        res -= MAX_UNSIGNED
    return res

def int2hex(data):
    if(data<0):
        data = 2**width+data
        bin_data = bin(data)
        bin_data = bin_data[2:len(bin_data)]
        hex_data = hex(int(bin_data,2))
        return '0x'+(hex_data.upper())[2:]
    else:
        bin_data = bin(data)
        bin_data = bin_data[2:len(bin_data)]
        for i in range(0,width-len(bin_data)):
            bin_data = '0' + bin_data
        hex_data = hex(int(bin_data,2))
        hex_data = hex_data[2:len(hex_data)]
        for i in range(0,int((width+3)/4)-len(hex_data)):
            hex_data = '0' + hex_data
        return '0x'+(hex_data).upper()