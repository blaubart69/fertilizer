#!/usr/bin/python3
import random

def stop():
    print ('fertilizer:stop()')
    return {'distance': 0, 'amount': 0, 'calculated': 0}

def reset():
    print ('fertilizer:reset()')
    return {'distance': 0, 'amount': 10, 'calculated': 10}

def calculate(data):
    print ('fertilizer:calculate()')
    print (data)
    distance = random.randint(35, 50)
    return {'distance': distance, 'amount': 10, 'calculated': 10}

def applyChanges(data):
    print ('fertilizer:applyChanges()')
    print (data)
    return {'distance': 0, 'amount': 10, 'calculated': 10}

