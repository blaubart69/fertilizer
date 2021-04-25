#!/usr/bin/python3
import json, web, calc

urls = (
    '/(.*)', 'RequestHandler'
)
app = web.application(urls, globals())

def calcCurrent():
    cal, dis, amo = calc.current()
    print(f"aktuell kg/ha: {cal:.1f}\tm: {dis:.1f}\tkg: \t{amo:.1f}\t{calc.currentDuenger}")
    return json.dumps({'calculated': cal, 'distance': dis, 'amount': amo, 'fertilizer': calc.currentDuenger})

class RequestHandler:

    def GET(self, path):
        if path == 'reset':
            calc.reset()
            return calcCurrent()
        elif path == 'calculate':
            return calcCurrent()
        else:
            raise web.seeother('/static/index.html')

    def POST(self, path):
        if path == 'applyChanges':
            fertilizer = web.data().decode('UTF-8')
            signals,kilo = calc.DuengerRatio[fertilizer]
            calc.setDuenger(fertilizer, signals, kilo)
            return calcCurrent()
        else:
            print ('Nothing')

if __name__ == "__main__":
    # fixed values for KALI
    calc.create(timespanMillisToWatch=20000)
    signals,kilo = calc.DuengerRatio["Kali"]
    calc.setDuenger("Kali",signals,kilo)
    app.run()
