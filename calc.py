#!/usr/bin/env python3
import time, buffer
#import calcdemo
import calcgpio

DuengerRatio = {
      "Kali"      : ( 30, 6.1  )
    , "Harnstoff" : ( 30, 4.0  )
    , "Phosphor"  : ( 30, 5.7 )
    , "KAS"       : ( 30, 5.55 )
}

_BCM_wheel  = 23
_BCM_roller = 24
_bufSizeSignals = 1024
METERS_PER_HEKTAR = 10000 / 15

_bufWheel  = buffer.SignalBuf(_bufSizeSignals)
_bufRoller = buffer.SignalBuf(_bufSizeSignals)
_timespanMillisToWatch = 5000

wheel_meter=50
wheel_signals=417
_signals_per_meter = wheel_signals / wheel_meter

_signals_per_kilo =  0

_lastMillis = 0

overallMeter = 0
overallKilo = 0
currentDuenger = "Kali"

def create(timespanMillisToWatch=5000):
    global _timespanMillisToWatch
    _timespanMillisToWatch = timespanMillisToWatch

    # !!! ATTENTION ATTENTION !!! switch between demo and gpio mode
    #calcdemo.setBuffer(_bufWheel, _bufRoller)
    #calcdemo.setup()
    calcgpio.setBuffer(_bufWheel, _bufRoller)
    calcgpio.setup()

def setDuenger(duenger_name, duenger_signals, duenger_kg):
    global _signals_per_kilo, currentDuenger
    currentDuenger = duenger_name
    _signals_per_kilo =  duenger_signals / duenger_kg

def reset():
    global overallKilo, overallMeter
    print("reset!!")
    overallMeter = 0
    overallKilo = 0

def checkSignals(cntWheel, cntRoller):
    #cntBadSignal = 0

    if cntWheel == 0:
        print("E: no signals from wheel")
        #cntBadSignal += 1
    if cntRoller == 0:
        print("E: no signals from roller")
        #cntBadSignal += 1

    #return (cntBadSignal == 0)

def current():
    global overallMeter, overallKilo, _lastMillis
    currentMillis = int(time.time() * 1000)

    signalsWheel  = _bufWheel.getSignalsWithinTimespan(timestampNow=currentMillis,  timespan=_timespanMillisToWatch)
    signalsRoller = _bufRoller.getSignalsWithinTimespan(timestampNow=currentMillis, timespan=_timespanMillisToWatch)
    print("signals wheel: {}\tsignals roller: {}, signal wheel overall: {}".format(signalsWheel, signalsRoller, _bufWheel.rbuf.overallSignals))

    #if checkSignals(signalsWheel, signalsRoller) == False:
    #    return 0,0,0
    checkSignals(signalsWheel, signalsRoller)

    meters_in_timespan = signalsWheel  / _signals_per_meter
    kilos_in_timespan  = signalsRoller / _signals_per_kilo

    if meters_in_timespan > 0:
        kilos_per_meter = kilos_in_timespan / meters_in_timespan
        kilo_per_ha     = kilos_per_meter * METERS_PER_HEKTAR
    else:
        kilo_per_ha = 0

    if _lastMillis != 0:
        millis_diff = currentMillis - _lastMillis   # 2,5s
        
        signalsWheel_lastDiff  = _bufWheel.getSignalsWithinTimespan(timestampNow=currentMillis,  timespan=millis_diff)
        signalsRoller_lastDiff = _bufRoller.getSignalsWithinTimespan(timestampNow=currentMillis, timespan=millis_diff)

        meter_since_last_refresh  = signalsWheel_lastDiff  / _signals_per_meter
        kilos_since_last_refresh  = signalsRoller_lastDiff / _signals_per_kilo

        overallMeter += meter_since_last_refresh
        overallKilo  += kilos_since_last_refresh

    _lastMillis = currentMillis

    return  kilo_per_ha, overallMeter, overallKilo
