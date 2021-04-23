#!/usr/bin/python3
import json, web, fertilizer, calc

urls = (
    '/(.*)', 'RequestHandler'
)
app = web.application(urls, globals())

def calcCurrent():
    cal, dis, amo = calc.current()
    print(f"aktuell kg/ha: {cal}\tm: {dis}\tkg: \t{amo}")
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
            return json.dumps(fertilizer.applyChanges(inputData))
        elif path == 'calculate':
            return calcCurrent()
        else:
            print ('Nothing')

if __name__ == "__main__":
    # fixed values for KALI
    calc.create(timespanMillisToWatch=20000, duenger_kg=6.1, duenger_signals=30, wheel_meter=50, wheel_signals=377)
    app.run()
