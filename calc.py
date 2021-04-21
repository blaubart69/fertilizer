#!/usr/bin/env python3

import time
#import RPi.GPIO as GPIO
import threading
import buffer

_BCM_wheel  = 23
_BCM_roller = 24
_bufSizeSignals = 1024
METERS_PER_HEKTAR = 10000 / 15

_bufWheel  = buffer.SignalBuf(_bufSizeSignals)
_bufRoller = buffer.SignalBuf(_bufSizeSignals)
_timespanMillisToWatch = 5000

_signals_per_meter = 0
_signals_per_kilo =  0

overallMeter = 0
overallKilo = 0

def create(timespanMillisToWatch=5000, duenger_kg=6.1, duenger_signals=30, wheel_meter=50, wheel_signals=377):
    global _timespanMillisToWatch, _signals_per_meter, _signals_per_kilo
    _timespanMillisToWatch = timespanMillisToWatch

    _signals_per_meter = wheel_signals   / wheel_meter
    _signals_per_kilo =  duenger_signals / duenger_kg

def getMillis():
    milliseconds = int(time.time() * 1000)
    return milliseconds


def _interrupt_callback(sig):
    timestampSignal = getMillis()

    #print("signal from {}".format(sig))

    if sig == _BCM_wheel:
        _bufWheel.tick(timestampSignal)
    elif sig == _BCM_roller:
        _bufRoller.tick(timestampSignal)
    else:
        print("signal from wrong pin {}".format(sig))

#   def setupGPIO():
#       GPIO.setmode(GPIO.BCM)
#       GPIO.setup(_BCM_wheel, GPIO.IN)
#       GPIO.add_event_detect(_BCM_wheel,  GPIO.FALLING, callback=_interrupt_callback)
#       GPIO.add_event_detect(_BCM_roller, GPIO.FALLING, callback=_interrupt_callback)

_fakeWheelDelay = 0.1
_fakeRollerDelay = 3.33

def fakeWheelSignal():
    _interrupt_callback(_BCM_wheel)
    threading.Timer(_fakeWheelDelay, fakeWheelSignal).start()

def fakeRollerSignal():
    _interrupt_callback(_BCM_roller)
    threading.Timer(_fakeRollerDelay, fakeRollerSignal).start()

def setupFakeGPIOsignals():
    print("setup fake signals...")
    threading.Timer(_fakeWheelDelay, fakeWheelSignal).start()
    threading.Timer(_fakeRollerDelay, fakeRollerSignal).start()
    print("setup fake signals...done")

def reset():
    global overallKilo, overallMeter
    print("reset!!")
    overallMeter = 0
    overallKilo = 0

def checkSignals(cntWheel, cntRoller):
    cntBadSignal = 0

    if cntWheel == 0:
        print("E: no signals from wheel")
        cntBadSignal += 1
    if cntRoller == 0:
        print("E: no signals from roller")
        cntBadSignal += 1

    return (cntBadSignal == 0)

def current():
    global overallMeter, overallKilo
    currentMillis = getMillis()
    signalsWheel  = _bufWheel.getSignalsWithinTimespan(timestampNow=currentMillis,  timespan=_timespanMillisToWatch)
    signalsRoller = _bufRoller.getSignalsWithinTimespan(timestampNow=currentMillis, timespan=_timespanMillisToWatch)
    print("signals wheel: {}\tsignals roller: {}".format(signalsWheel, signalsRoller))

    if checkSignals(signalsWheel, signalsRoller) == False:
        return 0,0,0

    meters_in_timespan = signalsWheel  / _signals_per_meter
    kilos_in_timespan  = signalsRoller / _signals_per_kilo

    overallMeter += meters_in_timespan
    overallKilo  += kilos_in_timespan

    kilos_per_meter = kilos_in_timespan / meters_in_timespan
    kilo_per_ha     = kilos_per_meter * METERS_PER_HEKTAR

    return  kilo_per_ha, overallMeter, overallKilo
