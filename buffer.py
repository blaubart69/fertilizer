#!/usr/bin/env python3

class RingBuf:
    def __init__(self,size):
        self.buf = [-1] * size
        self.idx = -1
        self.overallSignals = 0
        print(f"RingBuf.ctor self={self.idx}")

    def insert_timestamp(self,val):
        self.overallSignals += 1
        self.idx += 1
        if self.idx == len(self.buf):
            self.idx = 0
        self.buf[self.idx] = val

    def getIndex(self):
        return self.idx

class SignalBuf:
    def __init__(self, bufSize):
        self.ticks = 0
        self.rbuf = RingBuf(bufSize)

    def tick(self,timestamp):
        self.ticks += 1
        self.rbuf.insert_timestamp(timestamp)

    def getSignalsWithinTimespan(self, timestampNow, timespan):
        cnt=0
        readIdx = self.rbuf.idx
        #print("readIdx={}".format(readIdx))
        if readIdx == -1:
            return 0

        for i in range(len(self.rbuf.buf)):
            bufValue = self.rbuf.buf[readIdx]
            if bufValue == -1:
                return cnt

            diff = timestampNow - bufValue
            #print("bufValue: {}, diff: {}".format(bufValue,diff))
            if diff > timespan:
                return cnt
            else:
                cnt += 1
                readIdx = readIdx - 1
                if readIdx < 0:
                    readIdx = len(self.rbuf.buf)-1

        return -1
