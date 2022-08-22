import asyncio
import threading
import datetime
from time import time

from datetime import datetime
import calendar
import websockets
import json
import numpy as np
import requests


Tag2 = "70B3:D50F:7040:0498"  # Tag name
Tag1 = "70B3:D50F:7030:089B"  # Tag name

past= 0
pastDP= 0
x1= 0
y1= 0
z1 =0
Time=[]
coordinate=[]
Providerid=[]

#response = requests.get('http://192.168.8.1/rtls/json/device/all/stats')
#data = (response.json())
#print (data)
##a = len(data)
#for a in data:
  #  name = (a.get('mac'))
   # index = name.find('7010')
    #if index == -1:
     #   id = (a.get('hash'))
      #  Providerid.append(id)#
#print (Providerid)

async def localization1():
    # This section of the code is to access the Omlox system using Websocket
    async with websockets.connect('ws://192.168.8.1:8090/json/device/all/position') as websocket:
        response = await websocket.recv()
        objects = response.lstrip("[").rstrip("]")
       # start=time.perf_counter()

        def Device1():
            global past, pastDP,x1,y1,z1
            # The obtained response is in string format.The below code will remove the Square brackets from the fist
            # and last character

            # String to json conversion
            obj = json.loads(objects)
            #print(objects)
            providerid = (obj.get('provider_id'))
            #Timestamp = (obj.get('timestamp_generated'))
            #timestamps = str(Timestamp)[0:23]
            #if timestamps != "None":
                #Epoch= calendar.timegm(datetime.strptime(timestamps, "%Y-%m-%dT%H:%M:%S.%f").timetuple())
                #Time.insert(0,Epoch)
            Time = time()*1000
            present=Time[0]
            print("present:",present)
            a=len(Time)
            if a>1:
                past=Time[1]
                print("past:", past)

            timeA=past-present
            #print("Time:",timeA)

            # To access specific tag name
            if providerid == Tag1:
                #Obtainging the position and coordinates data
                positionNo = (obj.get('position'))
                coordinate.insert(0,(positionNo.get('coordinates')))
                c=len(coordinate)
                presentC=coordinate[0]
                x2= presentC[0]
                y2= presentC[1]
                z2=presentC[2]
                if c>1:
                    pastC = coordinate[1]
                    x1 = pastC[0]
                    y1 = pastC[1]
                    z1 = pastC[2]

                distance = np.sqrt(np.square((x1-x2))+ np.square((y1-y2))+ np.square((z1-z2)))
                limited_distance = "{:.3f}".format(distance)
                print("distance:",limited_distance)
                speed=(distance/timeA)
                limited_speed = "{:.3f}".format(speed)
                print("Speed:", limited_speed)

                #if x < 0.00 and y < 0:
                    #print("Location1: Out of Lab")
                #elif x > 2.410 and x <= 8.100:
                    #print("Location1: Working place in Lab")
                #elif x > 8.200 and x <= 10.000:
                    #print("Location1: Creative Room")
                #elif x <= 2.400:
                    #print("Location1: Festo Area")


        def Device2():
            global p21,p22
            # The obtained response is in string format.The below code will remove the Square brackets from the fist
            # and last character
            objects = response.lstrip("[").rstrip("]")
            # String to json conversion
            obj = json.loads(objects)
            providerid = (obj.get('provider_id'))

            # To access specific tag name
            if providerid == Tag2:
                #Obtainging the position and coordinates data
                positionNo = (obj.get('position'))
                coordinate = (positionNo.get('coordinates'))
                # print(coordinate)
                x = coordinate[0]
                y = coordinate[1]

                #if x < 0.00 and y < 0:
                    #print("Location2: Out of Lab")
                #elif x > 2.410 and x <= 8.100:
                    #print("Location2: Working place in Lab")
                #elif x > 8.200 and x <= 10.000:
                    #print("Location2: Creative Room")
                #elif x <= 2.400:
                    #print("Location2: Festo Area")
                #print('Tag-2 location:',p2)

        t1 = threading.Thread(target=Device1())
        t2 = threading.Thread(target=Device2())

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        #distance = np.sqrt(np.square((p11-p21))+ np.square((p12-p22)))
       # finish = time.perf_counter()
        #print(f'Finished in {round(finish-start,2)} seconds(s)')
        #time.sleep(2 )

while True:
    asyncio.get_event_loop().run_until_complete(localization1())
