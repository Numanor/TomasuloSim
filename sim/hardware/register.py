# -*- coding=utf-8 -*-

class Reg(object):
    
    def __init__(self, name):
        self.val = 0
        self.state = None
        self.name = name
    
    def getStatus(self, name):
        status = {'name': self.name}
        if self.state is None:
            status['state'] = ''
        elif isinstance(self.state, str):
            status['state'] = self.state
        else:
            status['state'] = self.state.name
        
        return status