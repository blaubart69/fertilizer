#!/usr/bin/env python3
import time, threading

_BCM_wheel  = 23
_BCM_roller = 24

_bufWheel  = None
_bufRoller = None

_fakeWheelDelay = 0.1
_fakeRollerDelay = 3.33

def setBuffer(bufWheel, bufRoller):
    global _bufWheel, _bufRoller
    _bufWheel = bufWheel
    _bufRoller = bufRoller

def _interrupt_callback(sig):
    timestampSignal = int(time.time() * 1000)

    if sig == _BCM_wheel:
        _bufWheel.tick(timestampSignal)
    elif sig == _BCM_roller:
        _bufRoller.tick(timestampSignal)
    else:
        print("signal from wrong pin {}".format(sig))

def fakeWheelSignal():
    _interrupt_callback(_BCM_wheel)
    threading.Timer(_fakeWheelDelay, fakeWheelSignal).start()

def fakeRollerSignal():
    _interrupt_callback(_BCM_roller)
    threading.Timer(_fakeRollerDelay, fakeRollerSignal).start()

def setup():
    print("setup fake signals...")
    threading.Timer(_fakeWheelDelay, fakeWheelSignal).start()
    threading.Timer(_fakeRollerDelay, fakeRollerSignal).start()
    print("setup fake signals...done")

