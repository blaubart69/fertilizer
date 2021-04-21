import time

class RingBuf:
    def __init__(self,size):
        self.buf = [0] * size
        self.idx = -1

    def insert(self,val):
        self.idx += 1
        if self.idx = len(self.buf):
            self.idx = 0
        self.buf[self.idx] = val

class SignalBuf:
    def __init__(self, bufSize):
        self.ticks = 0
        self.rbuf = RingBuf(bufSize)
    
    def tick(self,timestamp):
        self.ticks += 1
        self.rbuf.insert(timestamp)

