import queue
import asyncio
import requests
import time
import json
import calendar
import websockets
from datetime import datetime
import numpy as np
import time
import queue
import threading

coordinates=[]
Providerid=[]
past=0
s1 = 'http://192.168.8.1/rtls/json/device/'
s2 = '/position'
Coordinates_past=[]
Coordinates_present=[]
Time=[]
TimeA=0

response = requests.get('http://192.168.8.1/rtls/json/device/all')
data = (response.json())
print(data)
a = len(data)
for a in data:
    name = (a.get('mac'))
    index = name.find('7010')
    if index == -1:
        id = (a.get('hash'))
        Providerid.append(id)
print (Providerid)

past= 0
X1=0
X2=0
Y1=0
Y2=0
Z1=0
Z2=0
TimeA=0
speed=[]
async def localization1():
    # This section of the code is to access the Omlox system using Websocket
    async with websockets.connect('ws://192.168.8.1:8090/json/device/all/position') as websocket:
        global past, TimeA
        responsewb = await websocket.recv()
        objects = responsewb.lstrip("[").rstrip("]")
        obj = json.loads(objects)
        Timestamp = (obj.get('timestamp_generated'))
        timestamps = str(Timestamp)[0:23]
        if timestamps != "None":
            Epoch = calendar.timegm(datetime.strptime(timestamps, "%Y-%m-%dT%H:%M:%S.%f").timetuple())
            Time.insert(0, Epoch)
        present = Time[0]
        a = len(Time)
        if a > 2:
            past = Time[1]
            Time.pop()
        TimeA = present - past

        print(TimeA)
        def loop():
            global X2, Y2, TimeA, Z2
            ad = str(Providerid[3])
            newstring = s1+ad
            #print(newstring)
            pos = requests.get(newstring)
            datapos = (pos.json())
            motion = (datapos.get('motion'))
            if motion == True:
                posi = (datapos.get('position'))
                X1= posi.get('x')
                Y1= posi.get('y')
                Z1= posi.get('z')

                distance = np.sqrt(np.square((X1- X2)) + np.square((Y1 - Y2))+ np.square((Z1 - Z2)))
                X2 = X1
                Y2 = Y1
                Z2 = Z1
                
                print("Distance: ",distance)
                #print("Time:",TimeA)
                #Speed = distance/TimeA
                #print("Speed:","{:.3f}".format(Speed), 'm/s')
                #speed.insert(0,Speed)
                #print (speed)
        t1 = threading.Thread(target=loop())

        t1.start()
        time.sleep(2)
while True:
    asyncio.get_event_loop().run_until_complete(localization1())