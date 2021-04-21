#!/usr/bin/env python3

import time
import RPi.GPIO as GPIO

import SignalBuf

_BCM_wheel  = 23
_BCM_roller = 24

_bufSizeSignals = 1024

_bufWheel  = SignalBuf(_bufSizeSignals)
_bufRoller = SignalBuf(_bufSizeSignals)

def _interrupt_callback(sig):
	global _bufWheel,_bufRoller

    timestampSignal = time.monotonic_ns()

    if sig == _BCM_wheel:
	    _bufWheel.insert(timestampSignal)
    elif sig == _BCM_roller:
        _bufRoller.insert(timestampSignal)
    else:
        print("signal from wrong pin {}".format(sig));

def setupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BCM_wheel, GPIO.IN)
    GPIO.add_event_detect(_BCM_wheel,  GPIO.FALLING, callback=_interrupt_callback)
    GPIO.add_event_detect(_BCM_roller, GPIO.FALLING, callback=_interrupt_callback)

def reset():
	global _bufWheel,_bufRoller
    _bufWheel  = SignalBuf(_bufSizeSignals)
    _bufRoller = SignalBuf(_bufSizeSignals)
