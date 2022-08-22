import asyncio
import time
import websockets
import json

# saving the MAC address if the omlox tag in a variable
Tag = "70B3:D50F:7030:089B"

async def localize():
    # Accessing the Omlox system using Websocket
    async with websockets.connect('ws://172.21.5.224:8090/json/device/all/position') as websocket:
        response = await websocket.recv()

        # The obtained response is in string format.
        # The below code will remove the Square brackets from the fisrt and last character
        objects = response.lstrip("[").rstrip("]")

        # Convert String to json
        obj = json.loads(objects)
        providerid = (obj.get('provider_id'))

        # Filter for speciic TAG (MAC)
        if providerid == Tag:

            # Obtainging the position and coordinates data
            positionNo = (obj.get('position'))
            coordinate = (positionNo.get('coordinates'))
            # print(coordinate)

            # Depending on the X cordinates (because the three zones are splited only vertically) the loop will perform area operation
            x = coordinate[0]
            y = coordinate[1]

            if x < 0.00 and y < 0:
                print("Location: Out of Lab")
            elif x > 2.410 and x <= 8.100:
                print("Location: Working place in Lab")
            elif x > 8.200 and x <= 10.000:
                print("Location: Creative Room")
            elif x <= 2.400:
                print("Location: Festo Area")
            time.sleep(2)

while True:
    asyncio.get_event_loop().run_until_complete(localize())
