import time

class RingBuf:
    def __init__(self,size):
        self.buf = [0] * size
        self.idx = 0

    def insert(self,val):
        if self.idx >= len(self.buf):
            self.idx = 0
        self.buf[self.idx] = val
        self.idx += 1

class SigCounter:
    def __init__(self, bufSize):
        self.ticks = 0
        self.rbuf = RingBuf(bufSize)
    
    def tick(self):
        self.ticks += 1
        self.rbuf.insert(time.monotonic_ns())

sc = SigCounter(1024)
sc.tick()
