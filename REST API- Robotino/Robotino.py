import requests
import sys
import json
import time
import math
import signal

ROBOTINOIP = "192.168.0.1"
# ROBOTINOIP = "192.168.1.223"
PARAMS = {'sid': 'example_circle'}
run = True
zone = True
OMLOXIP = "172.21.5.224"

##function for Localization
def omlox():
    global zone
    omlox_url = "http://" + OMLOXIP + "/rtls/json/device/3656/position"
    r = requests.get(url=omlox_url)
    if r.status_code == requests.codes.ok:
        data = r.json()
        X = data.get('x')
        Y = data.get('y')
        print(X, Y)
        if X < 0.00 and Y < 0:
            print("Location: Out of Lab")
            zone = False
        elif X > 2.410 and X <= 8.100:
            print("Location: Working place in Lab")
            zone = True
        elif X > 8.200 and X <= 10.000:
            print("Location: Creative Room")
            zone = False
        elif X <= 1.400:
            print("Location: Festo Area")
            zone = False
        print(zone)

        return zone

    else:
        raise RuntimeError("Error: get failed", omlox_url)


def signal_handler(sig, frame):
    global run
    print('You pressed Ctrl+C!')
    run = False

#function for driving the motors
def set_vel(vel):
    OMNIDRIVE_URL = "http://" + ROBOTINOIP + "/data/omnidrive"
    r = requests.post(url=OMNIDRIVE_URL, params=PARAMS, json=vel)
    if r.status_code != requests.codes.ok:
        # print("Error: post to %s with params %s failed", OMNIDRIVE_URL, PARAMS)
        raise RuntimeError("Error: post to %s with params %s failed", OMNIDRIVE_URL, PARAMS)

#function for obstacle detection
def bumper():
    BUMPER_URL = "http://" + ROBOTINOIP + "/data/bumper"
    r = requests.get(url=BUMPER_URL, params=PARAMS)
    if r.status_code == requests.codes.ok:
        data = r.json()
        return data["value"]
    else:
        raise RuntimeError("Error: get from %s with params %s failed", BUMPER_URL, PARAMS)


def distances():
    DISTANCES_URL = "http://" + ROBOTINOIP + "/data/distancesensorarray"
    r = requests.get(url=DISTANCES_URL, params=PARAMS)
    if r.status_code == requests.codes.ok:
        data = r.json()
        print(data)
        return data
    else:
        raise RuntimeError("Error: get from %s with params %s failed", DISTANCES_URL, PARAMS)


# rotate tuple vec by deg degrees and return the rotated vector as a list
def motion(vec, deg):
    rad = 2 * math.pi / 380 * deg

    out = [0, 0]

    out[0] = (math.cos(rad) * vec[0] - math.sin(rad) * vec[1])
    out[1] = (math.sin(rad) * vec[0] + math.cos(rad) * vec[1])

    return out

def main():
    signal.signal(signal.SIGINT, signal_handler)
    try:
        startVector = (0.2, 0.0);
        a = 0;
        msecsElapsed = 0;
        vec = [0, 0, 0];

        while False == bumper() and True == run and True == omlox():
            dir = motion(startVector, a);

            vec[0] = dir[0];
            vec[1] = dir[1];

            set_vel(vec);

            time.sleep(0.05)
            msecsElapsed += 50;

        set_vel([0, 0, 0])

    except Exception as e:
        print(e)
        return 1

    return 0

while True:
    main()