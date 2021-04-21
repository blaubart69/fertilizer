#!/usr/bin/env python3

import time
#import RPi.GPIO as GPIO
import threading

from signalBuf import SignalBuf 

def getMillis():
    milliseconds = int(time.time() * 1000)
    return milliseconds

class Calc:

    _BCM_wheel  = 23
    _BCM_roller = 24
    _bufSizeSignals = 1024
    METERS_PER_HEKTAR = 10000 / 15

    def __init__(self,timespanMillisToWatch,duenger_kg, duenger_signals, wheel_meter, wheel_signals):

        self._bufWheel  = SignalBuf(self._bufSizeSignals)
        self._bufRoller = SignalBuf(self._bufSizeSignals)
        self._timespanMillisToWatch = timespanMillisToWatch

        self._signals_per_meter = wheel_signals   / wheel_meter
        self._signals_per_kilo =  duenger_signals / duenger_kg

        self.overallMeter = 0
        self.overallKilo = 0

    def _interrupt_callback(self,sig):
        timestampSignal = getMillis()

        #print("signal from {}".format(sig))

        if sig == self._BCM_wheel:
            self._bufWheel.tick(timestampSignal)
        elif sig == self._BCM_roller:
            self._bufRoller.tick(timestampSignal)
        else:
            print("signal from wrong pin {}".format(sig))

 #   def setupGPIO(self):
 #       GPIO.setmode(GPIO.BCM)
 #       GPIO.setup(self._BCM_wheel, GPIO.IN)
 #       GPIO.add_event_detect(self._BCM_wheel,  GPIO.FALLING, callback=_interrupt_callback)
 #       GPIO.add_event_detect(self._BCM_roller, GPIO.FALLING, callback=_interrupt_callback)

    _fakeWheelDelay = 0.1
    _fakeRollerDelay = 0.3

    def fakeWheelSignal(self):
        self._interrupt_callback(self._BCM_wheel)
        threading.Timer(self._fakeWheelDelay, self.fakeWheelSignal).start()

    def fakeRollerSignal(self):
        self._interrupt_callback(self._BCM_roller)
        threading.Timer(self._fakeRollerDelay, self.fakeRollerSignal).start()

    def setupFakeGPIOsignals(self):
        print("setup fake signals...")
        threading.Timer(self._fakeWheelDelay, self.fakeWheelSignal).start()
        threading.Timer(self._fakeRollerDelay, self.fakeRollerSignal).start()
        print("setup fake signals...done")

    def reset(self):
        self._bufWheel  = SignalBuf(_bufSizeSignals)
        self._bufRoller = SignalBuf(_bufSizeSignals)

    def checkSignals(self,cntWheel, cntRoller):
        cntBadSignal = 0

        if cntWheel == 0:
            print("E: no signals from wheel")
            cntBadSignal += 1
        if cntRoller == 0:
            print("E: no signals from roller")
            cntBadSignal += 1

        return (cntBadSignal == 0)

    def current(self):
        currentMillis = getMillis()
        signalsWheel  = self._bufWheel.getSignalsWithinTimespan(timestampNow=currentMillis,  timespan=self._timespanMillisToWatch)
        signalsRoller = self._bufRoller.getSignalsWithinTimespan(timestampNow=currentMillis, timespan=self._timespanMillisToWatch)
        print("signals wheel: {}\tsignals roller: {}".format(signalsWheel, signalsRoller))

        if self.checkSignals(signalsWheel, signalsRoller) == False:
            return 0,0,0

        meters_in_timespan = signalsWheel  / self._signals_per_meter
        kilos_in_timespan  = signalsRoller / self._signals_per_kilo

        self.overallMeter += meters_in_timespan
        self.overallKilo  += kilos_in_timespan

        kilos_per_meter = kilos_in_timespan / meters_in_timespan
        kilo_per_ha     = kilos_per_meter * self.METERS_PER_HEKTAR

        return  kilo_per_ha, self.overallMeter, self.overallKilo
