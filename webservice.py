#!/usr/bin/python3
import json, web, fertilizer

import calc

urls = (
    '/(.*)', 'RequestHandler'
)
app = web.application(urls, globals())
_calc = calc.Calc(timespanMillisToWatch=5000, duenger_kg=6.1, duenger_signals=20, wheel_meter=50, wheel_signals=377)

class RequestHandler:

    def GET(self, path):
        if path == '':
            raise web.seeother('/static/index.html')
        elif path == 'stop':
            return json.dumps(fertilizer.stop())
        elif path == 'reset':
            _calc.reset()
            return json.dumps(fertilizer.reset())

    def POST(self, path):
        #inputData = json.loads(web.data())
        if path == 'applyChanges':
            return json.dumps(fertilizer.applyChanges(inputData))
        elif path == 'calculate':
            currentKiloPerHa, overallDistanceMeter, overallKilo = _calc.current()
            print("aktuell kg/ha: {}\tkg: \t{}\tm: {}".format(currentKiloPerHa, overallDistanceMeter, overallKilo))
            return json.dumps({'distance': overallDistanceMeter, 'amount': overallKilo, 'calculated': currentKiloPerHa})
            #return json.dumps(fertilizer.calculate(inputData))
        else:
            print ('Nothing')

if __name__ == "__main__":
    # _calc.setupGPIO()
    _calc.setupFakeGPIOsignals()
    app.run()
	