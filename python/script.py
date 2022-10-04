from http.client import responses
from re import T
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish 
import time
import threading
import logging
import json
import random
import glob, os
from datetime import datetime
import schedule
# open json file with device information
# f = open("./config.json")

# data from first line

# with open("C:\\Users\lucal\Desktop\Lower.txt","r") as m:
#     acquired = m.readline()
# print(acquired)
# date_time_obj = acquired.split()
# u = date_time_obj[2]+" "+date_time_obj[4]
# print("date :" + str(datetime.strptime(u, "%m/%d/%Y %H:%M:%S").strftime('%m/%d/%y')))

# /data from first line

# scan file in folder

# list_of_files = glob.glob('C:/Users/lucal/Desktop/test_DIGISTONE_piattaforma/*.txt') 
# latest_file = max(list_of_files, key = os.path.getctime)
# # for file in glob.glob("*.txt"):
# #     print(file)
# print(latest_file)

# # /scan file in folder


# # Reading file txt for mesurements
# path = "C:/Users/lucal/Desktop/test_DIGISTONE_piattaforma/"+latest_file
# fileNameToSend = path.split("\\")
# fM = open(latest_file,"r")
# name = "Lower"
# arrayData = []
# for i, line in enumerate(fM):
#     if i >= 28 and i <= 109:
#     # if i == 28:
#         arrayData.append({
#             "line": i,
#             "data":line.split()
#         })

# fM.close()

# data = json.load(f)

# # creazione client mqtt
# clients = []
# count = 0


# # create an array of clients with data from config file
# for device in data["devices"]:
#     clients.append({
#         "id": device["id"],
#         "broker": "127.0.0.1",
#         "port": 1883,
#         "name": device["name"],
#         "username": device["token"],
#     })

# nclients=len(clients)




# c = mqtt.Client(
#     client_id = "mqtt-client-"+ str(clients[0]["id"]),
#     clean_session=True,
#     userdata=None,
#     protocol=mqtt.MQTTv31,
#     transport="tcp"
# )

# c.username_pw_set(username=clients[0]["username"])
# c.broker = clients[0]["broker"]
# c.port = clients[0]["port"]
# c.topic = "#"
# c.keepalive = 60

autha = {
    'username':"YyqqXz3Pzib6omC7FOLj"
}


def sendData(arrayData,fileNameToSend):
    c = 0
    for data in arrayData:
    # print(len(data["data"]))
        if len(data["data"]) == 3:

            send = {
                "length": float(data["data"][0]),
                "temperature_change": float(data["data"][1]),
                "strain": float(data["data"][2]),
                "file": str(fileNameToSend)
            }
            publish.single(topic="v1/devices/me/telemetry", payload=json.dumps(send), hostname="localhost", client_id="mqtt-client-1", keepalive=60, will=None, tls=None,protocol=mqtt.MQTTv311, transport="tcp", port=1883, auth= autha)
            time.sleep(5)
            c +=1
            print("cose in arrayData "+ str(float(data["data"][0])))
            print("cose in arrayData1 "+ str(float(data["data"][1])))
            print("cose in arrayData2 "+ str(float(data["data"][2])))
            print("count "+ str(c))
        else: 
            pass


def grabFile():
    arrayData = []

    list_of_files = glob.glob('C:/Users/lucal/Desktop/test_DIGISTONE_piattaforma/*.txt') 
    for file in list_of_files:
        if "lower" in file.lower() and "examinated" not in file.lower():
            print("file"+str(file))
            #dopo aver fatto tutte le cose che devo fare con il file gli cambio il nome
            path = "C:/Users/lucal/Desktop/test_DIGISTONE_piattaforma/"+file
            fM = open(file,"r")
            fileNameToSend = file.split("\\")[1].split(".")[0]
            for i, line in enumerate(fM):
                if i >= 28 and i <= 109:
                # if i == 28:
                    arrayData.append({
                        "line": i,
                        "data":line.split()
                    })
            fM.close()
            sendData(arrayData, fileNameToSend)
            arrayData = []
            fileNameToModify = "C:/Users/lucal/Desktop/test_DIGISTONE_piattaforma/"+file.split("\\")[1].split(".")[0]+"_examinated.txt"
            os.rename(file, fileNameToModify)
    # latest_file = max(list_of_files, key = os.path.getctime)
    # # for file in glob.glob("*.txt"):
    # #     print(file)
    # print(latest_file)

    # /scan file in folder


    # Reading file txt for mesurements
    # path = "C:/Users/lucal/Desktop/test_DIGISTONE_piattaforma/"+fileNameToModify
    # fileNameToSend = path.split("\\")
    # fM = open(latest_file,"r")
    # name = "Lower"
    # arrayData = []
    # for i, line in enumerate(fM):
    #     if i >= 28 and i <= 109:
    #     # if i == 28:
    #         arrayData.append({
    #             "line": i,
    #             "data":line.split()
    #         })

    # fM.close()
    

schedule.every(0.1).minutes.do(grabFile)


while True:
     
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)