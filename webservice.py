#!/usr/bin/python3
import json, web, fertilizer

import calc

urls = (
    '/(.*)', 'RequestHandler'
)
app = web.application(urls, globals())

class RequestHandler:

    def GET(self, path):
        if path == '':
            raise web.seeother('/static/index.html')
        elif path == 'stop':
            return json.dumps(fertilizer.stop())
        elif path == 'reset':
            calc.reset()
            return json.dumps(fertilizer.reset())

    def POST(self, path):
        inputData = json.loads(web.data())
        if path == 'applyChanges':
            return json.dumps(fertilizer.applyChanges(inputData))
        elif path == 'calculate':
            return json.dumps(fertilizer.calculate(inputData))
        else:
            print ('Nothing')

if __name__ == "__main__":
    calc.setupGPIO()
    app.run()
	