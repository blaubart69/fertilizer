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

def loadSettings():
    with open('./conf/duenger.json','r') as f: 
      duenger_json = f.read()
    return duenger_json

def saveSettings(jsonInput):
    with open('./conf/duenger.json', 'w') as outfile: 
      outfile.write(jsonInput)

def applySettings():
    jsonRationString = loadSettings()
    jsonDuengerRatio = json.loads(jsonRationString)
    print(jsonDuengerRatio)
    calc.setDuengerRatio(jsonDuengerRatio)

class RequestHandler:

    def GET(self, path):
        if path == 'reset':
            calc.reset()
            return calcCurrent()
        elif path == 'calculate':
            return calcCurrent()
        elif path == 'settings':
            return loadSettings()
        else:
            raise web.seeother('/static/index.html')

    def POST(self, path):
        if path == 'applyChanges':
            fertilizer = web.data().decode('UTF-8')
            signals,kilo = calc.DuengerRatio[fertilizer]
            calc.setDuenger(fertilizer, signals, kilo)
            return calcCurrent()
        elif path == 'settings':
            print('Store settings')
            newSettings_json_string = web.data().decode('UTF-8')
            print(newSettings_json_string)
            saveSettings(newSettings_json_string)
            calc.setDuengerRatio( json.loads(newSettings_json_string) )       
        else:
            print ('Nothing')

if __name__ == "__main__":
    # fixed values for KALI
    calc.create(timespanMillisToWatch=20000)

    applySettings()

    signals,kilo = calc.DuengerRatio["Kali"]
    calc.setDuenger("Kali",signals,kilo)
    app.run()
