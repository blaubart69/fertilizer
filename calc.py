#!/usr/bin/env python3

import time
import RPi.GPIO as GPIO

_BCM_wheel  = 23
_BCM_roller = 24

_cnt_signal_wheel  = 0
_cnt_signal_roller = 0

_bufWheel  = [0]*1024
_bufRoller = [0]*1024 

def _signal_wheel(sig):
	global _cnt_signal_wheel
	_cnt_signal_wheel += 1

def _signal_roller(sig):
	global _cnt_signal_roller
	_cnt_signal_roller += 1

def setupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BCM_wheel, GPIO.IN)
    GPIO.add_event_detect(_BCM_wheel, GPIO.FALLING, callback=_signal_wheel)
    GPIO.add_event_detect(_BCM_wheel, GPIO.FALLING, callback=_signal_roller)

def resetCounters():
    global _cnt_signal_roller, _cnt_signal_wheel, _bufRoller, _bufWheel
    _cnt_signal_wheel = 0
    _cnt_signal_roller = 0
    _bufRoller = [0]*1024
    _bufWheel  = [0]*1024

