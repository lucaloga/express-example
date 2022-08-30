from http.client import responses
from re import T
import paho.mqtt.client as mqtt
import time
import threading
import logging
import json
import random

from datetime import datetime

# open json file with device information
f = open("./config.json")

# data from first line

# with open("C:\\Users\lucal\Desktop\Lower.txt","r") as m:
#     acquired = m.readline()
# print(acquired)
# date_time_obj = acquired.split()
# u = date_time_obj[2]+" "+date_time_obj[4]
# print("date :" + str(datetime.strptime(u, "%m/%d/%Y %H:%M:%S").strftime('%m/%d/%y')))

# /data from first line

# Reading file txt for mesurements
fM = open("C:\\Users\lucal\Desktop\Lower.txt","r")
arrayData = []
for i, line in enumerate(fM):
    # if i >= 29 and i <= 35:
    if i == 29:
        arrayData.append({
            "line": i,
            "data":line.split()
        })

fM.close()

data = json.load(f)

# creazione client mqtt
clients = []
count = 0

# increment a count to controll if client send the correct number of messages
def increment():
    global COUNT
    COUNT = COUNT+1

# create an array of clients with data from config file
for device in data["devices"]:
    clients.append({
        "id": device["id"],
        "broker": "127.0.0.1",
        "port": 1883,
        "name": device["name"],
        "username": device["token"],
    })

nclients=len(clients)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        for data in arrayData:
            # print(len(data["data"]))
            if len(data["data"]) == 6:

                send = {
                    "length": float(data["data"][0]),
                    "strain": float(data["data"][5])
                    }
                # print("l", send["length"])
                # print("s", send["strain"])
                client.publish(topic="v1/devices/me/telemetry", payload=json.dumps(send))
            else: 
                pass
        # when client do a publish the count are incremented
            global count
            count=count+1
    else:
        pass

def on_message(client, userdata, msg):
    pass

def on_publish(client, userdata, result):
    # print(result)
    pass
# clients functions

devices = []
threads = []
# a function that instace the clients form array and append in an array of threads
def Create_clients():
    for client in clients:
        c = mqtt.Client(
            client_id = "mqtt-client-"+ str(client["id"]),
            clean_session=True,
            userdata=None,
            protocol=mqtt.MQTTv31,
            transport="tcp"
        )
        c.username_pw_set(username=client["username"])
        c.broker = client["broker"]
        c.port = client["port"]
        c.topic = "#"
        c.keepalive = 60
        c.on_connect = on_connect
        c.on_message = on_message
        c.on_publish = on_publish
        c.connect(c.broker, c.port, c.keepalive)
        devices.append(c)
        cThread = threading.Thread(target=c.loop_start)
        cThread.deamon = True
        threads.append(cThread)
        cThread.start()


Create_clients()
# a loop that waits for count
loop = True
while loop:
    if count == len(clients):
        data = "ok"
        for t in threads:
            t._stop()
        loop = False
        print(data)