#!/usr/bin/python3
import json, web, fertilizer, calc

urls = (
    '/(.*)', 'RequestHandler'
)
app = web.application(urls, globals())


def calcCurrent():
    currentKiloPerHa, overallDistanceMeter, overallKilo = calc.current()
    print("aktuell kg/ha: {}\tkg: \t{}\tm: {}".format(currentKiloPerHa, overallDistanceMeter, overallKilo))
    return json.dumps({'distance': overallDistanceMeter, 'amount': overallKilo, 'calculated': currentKiloPerHa})

class RequestHandler:

    def GET(self, path):
        if path == '':
            raise web.seeother('/static/index.html')
        elif path == 'stop':
            return json.dumps(fertilizer.stop())
        elif path == 'reset':
            calc.reset()
            return calcCurrent()

    def POST(self, path):
        inputData = json.loads(web.data())
        if path == 'applyChanges':
            return json.dumps(fertilizer.applyChanges(inputData))
        elif path == 'calculate':
            return calcCurrent()
        else:
            print ('Nothing')

if __name__ == "__main__":
    # _calc.setupGPIO()
    calc.setupFakeGPIOsignals()    
    # fixed values for KALI
    calc.create(timespanMillisToWatch=20000, duenger_kg=6.1, duenger_signals=30, wheel_meter=50, wheel_signals=377)
    app.run()