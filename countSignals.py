#!/usr/bin/env python3

import signal
import time
import RPi.GPIO as GPIO

cnt_signal_wheel = 0

def signal_wheel(sig):
	global cnt_signal_wheel
	cnt_signal_wheel += 1

BCM_wheel  = 23
BCM_roller = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(BCM_wheel, GPIO.IN)
GPIO.add_event_detect(BCM_wheel, GPIO.FALLING, callback=signal_wheel)

last_cnt_signal_wheel = 0
while True:
    time.sleep(0.001)
    if cnt_signal_wheel > last_cnt_signal_wheel:
        print(cnt_signal_wheel)
        last_cnt_signal_wheel=cnt_signal_wheel

