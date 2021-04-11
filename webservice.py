#!/usr/bin/python3
import json, web, fertilizer

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
            return json.dumps(fertilizer.reset())
        elif path == 'calculate':
            return json.dumps(fertilizer.calculate())

    def POST(self, path):
        inputData = json.loads(web.data())
        if path == 'applyChanges':
            return json.dumps(fertilizer.applyChanges(inputData))
        else:
            print ('Nothing')

if __name__ == "__main__":
    app.run()
	