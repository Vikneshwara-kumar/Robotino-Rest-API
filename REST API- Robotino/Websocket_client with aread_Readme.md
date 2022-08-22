# Introduction

WebSocket protocol is a TCP - based network protocol which is designed to establish bidirectional connection between a
web application and a WebSocket server or a web server that support websockets.

## Installation and configuration

You can use either `python3 setup.py install` or `pip3 install webSocket to install`. This module is 
tested on Python 3.9.6
 
There are other dependencies that has  to be installed to run the code.
In this code we will be working with json files, so we need to install  json library `pip install jsons`

We need asyncio module which provides infrastructure for writing single-threaded concurrent code using coroutines, 
multiplexing I/O access over sockets.`pip install asyncio`

## Steps
1) Start the omlox system
2) Connect your PC or System to the omlox server using wifi 
3) Using the given address we can access the omlox server 'ws://192.168.8.1:8090/json/device/all/position'
   the ip address can be changed using the admin access. So before, running the code check the ip address in the code.
4) Run the code

##These are the areas defined with respect to coordinates.

here x is the realtime cordinates and the defined values are the boundries of each area
1) Festo area (area-1)
   x <= 2.400
2) Working place area (area-2) 
   x > 2.410 and x <= 8.100
3) Creative room area (area-3)
   x > 8.200 and x <= 10.000

### Note
The data obtained from the omlox system was in string format. It had [] in the start and end of the string. when it was 
converted into json, its type was changed to list. Because of this accessing the obtained data became difficult. So 
before converting sting to json, the [] was removed using `objects = response.lstrip("[").rstrip("]")`.
After this it was easy to access the dictionary. 


