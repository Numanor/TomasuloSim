# -*- coding=utf-8 -*-

class FuncUnit(object):

    def __init__(self, name):
        self.remain = 0
        self.name = name
        self.rs = None
    
    def clear(self):
        self.rs = None

class FU_Add(FuncUnit):

    def __init__(self, name):
        FuncUnit.__init__(self, name)

class FU_Mult(FuncUnit):

    def __init__(self, name):
        FuncUnit.__init__(self, name)

class FU_Load(FuncUnit):

    def __init__(self, name):
        FuncUnit.__init__(self, name)
