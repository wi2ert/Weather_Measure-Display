class Dmo:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.t = 0
        self.h = 0
        self.p = 0
        self.l = 0
        self.c = 0
    
    def add(self, t, h, p, l):
        self.t += t
        self.h += h
        self.p += p
        self.l += l
        self.c += 1