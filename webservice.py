#!/usr/bin/python3
import json, web, fertilizer, calc

urls = (
    '/(.*)', 'RequestHandler'
)
app = web.application(urls, globals())

def calcCurrent():
    cal, dis, amo = calc.current()
    print(f"aktuell kg/ha: {cal:.1f}\tm: {dis:.1f}\tkg: \t{amo:.1f}")
    return json.dumps({'calculated': cal, 'distance': dis, 'amount': amo, 'distancePerDay': dis / 1000 + 5, 'amountPerDay': amo + 500})

class RequestHandler:

    def GET(self, path):
        if path == 'stop':
            return json.dumps(fertilizer.stop())
        elif path == 'reset':
            calc.reset()
            return calcCurrent()
        else:
            raise web.seeother('/static/index.html')

    def POST(self, path):
        inputData = json.loads(web.data())
        if path == 'applyChanges':
            signals,kilo = calc.DuengerRatio[inputData.fertilizer]
            calc.setDuenger(inputData.fertilizer, signals, kilo)
            return calcCurrent()
        elif path == 'calculate':
            return calcCurrent()
        else:
            print ('Nothing')

if __name__ == "__main__":
    # fixed values for KALI
    calc.create(timespanMillisToWatch=20000)
    signals,kilo = calc.DuengerRatio["Kali"]
    calc.setDuenger("Kali",signals,kilo)
    app.run()
