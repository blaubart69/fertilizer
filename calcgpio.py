#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO

_BCM_wheel  = 23
_BCM_roller = 24

_bufWheel  = None
_bufRoller = None

def _interrupt_callback(sig):
    timestampSignal = int(time.time() * 1000)

    if sig == _BCM_wheel:
        _bufWheel.tick(timestampSignal)
    elif sig == _BCM_roller:
        _bufRoller.tick(timestampSignal)
    else:
        print("signal from wrong pin {}".format(sig))

def setup(bufWheel, bufRoller):
    global _bufWheel, _bufRoller
    _bufWheel = bufWheel
    _bufRoller = bufRoller
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(_BCM_wheel, GPIO.IN)
    GPIO.setup(_BCM_roller, GPIO.IN)
    GPIO.add_event_detect(_BCM_wheel,  GPIO.FALLING, callback=_interrupt_callback)
    GPIO.add_event_detect(_BCM_roller, GPIO.FALLING, callback=_interrupt_callback)
