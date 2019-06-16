# -*- coding=utf-8 -*-

class Reg(object):
    
    def __init__(self, name):
        self.val = '0x0'
        self.state = None
        self.name = name
    
    def getStatus(self):
        status = {'name': self.name}
        if self.state is None:
            status['state'] = self.val
        else:
            status['state'] = self.state.name
        return status