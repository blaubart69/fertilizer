#!/usr/bin/python3

def stop():
    print ('fertilizer:stop()')
    return {'distance': 0, 'amount': 0, 'calculated': 0}

def reset():
    print ('fertilizer:reset()')
    return {'distance': 0, 'amount': 10, 'calculated': 10}

def calculate():
    print ('fertilizer:calculate()')
    return {'distance': 45, 'amount': 10, 'calculated': 10}

def applyChanges(data):
    print ('fertilizer:applyChanges()')
    print (data)
    return {'distance': 0, 'amount': 10, 'calculated': 10}

