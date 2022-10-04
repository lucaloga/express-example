import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from time import sleep
import random

broker="localhost"
topic_pub='v1/devices/me/telemetry'


client = mqtt.Client(
            client_id = "mqtt-client-1",
            clean_session=True,
            userdata=None,
            protocol=mqtt.MQTTv31,
            transport="tcp"
)
autha = {
    'username':"3BBXHtMjOCALRNpHXSwA"
}

client.username_pw_set("3BBXHtMjOCALRNpHXSwA")
# client.connect('localhost', 1883, 1)

for i in range(5):
    x = random.randrange(20, 100)
    print(x)
    msg = '{"windSpeed":"'+ str(x) + '"}'
    publish.single(topic_pub, payload=msg, hostname="localhost", client_id="mqtt-client-1", keepalive=60, will=None, tls=None,
    protocol=mqtt.MQTTv311, transport="tcp", port=1883, auth= autha)
    # client.connect('localhost', 1883, 1)
    # client.loop_start()
    # client.publish(topic_pub, msg)
    sleep(5)
    # client.disconnect()
    
    # sleep(2)

# cm = 0
# def on_connect(client, userdata, flags, rc):
#     global cm
#     if rc == 0:
#         for data in arrayData:
#             # print(len(data["data"]))
#             if len(data["data"]) == 3:

#                 send = [{
#                     "length": float(data["data"][0]),
#                     "temperature_change": float(data["data"][1]),
#                     "strain": float(data["data"][2]),
#                     "file": fileNameToSend[1].split(".")[0],
#                     "count": cm
#                     }]
#                 # print(send["file"])
#                 # print("l", send["length"])
#                 # print("s", send["strain"])
#                 # time.sleep(0.5)
#                 client.publish(topic="v1/devices/me/telemetry", payload=json.dumps(send))
#                 time.sleep(5)
#                 cm += 1
#                 print("count", cm)
#                 print("cose in arrayData "+ str(data["data"][0]))
#                 print("cose in arrayData1 "+ str(data["data"][1]))
#                 print("cose in arrayData2 "+ str(data["data"][2]))
#             else: 
#                 pass
#         # when client do a publish the count are incremented
#             global count
#             count=count+1
#         client.disconnect()
#     else:
#         pass

# def on_message(client, userdata, msg):
#     pass

# def on_publish(client, userdata, result):
#     # print(result)
#     # print("client"+ str(client["id"]))
#     # print("userdata"+ userdata)
#     pass
# # clients functions

# devices = []
# threads = []
# # a function that instace the clients form array and append in an array of threads
# def Create_clients():
#     for client in clients:
#         c = mqtt.Client(
#             client_id = "mqtt-client-"+ str(client["id"]),
#             clean_session=True,
#             userdata=None,
#             protocol=mqtt.MQTTv31,
#             transport="tcp"
#         )
#         c.username_pw_set(username=client["username"])
#         c.broker = client["broker"]
#         c.port = client["port"]
#         c.topic = "#"
#         c.keepalive = 60
#         c.on_connect = on_connect
#         c.on_message = on_message
#         c.on_publish = on_publish
#         c.connect(c.broker, c.port, c.keepalive)
#         devices.append(c)
#         cThread = threading.Thread(target=c.loop_start)
#         cThread.deamon = True
#         threads.append(cThread)
#         cThread.start()


# # Create_clients()
# # a loop that waits for count
# # loop = True
# # while loop:
# #     if count == len(clients):
# #         data = "ok"
# #         for t in threads:
# #             t._stop()
# #         loop = False
# #         print(data)

# c = mqtt.Client(
#             client_id = "mqtt-client-"+ str(clients[0]["id"]),
#             clean_session=True,
#             userdata=None,
#             protocol=mqtt.MQTTv31,
#             transport="tcp"
#         )
# c.username_pw_set(username=clients[0]["username"])
# c.broker = clients[0]["broker"]
# c.port = clients[0]["port"]
# c.topic = "#"
# c.keepalive = 60
# c.on_connect = on_connect
# c.on_message = on_message
# c.on_publish = on_publish
# c.connect(c.broker, c.port, c.keepalive)
# c.loop_forever()

# increment a count to controll if client send the correct number of messages
# def increment():
#     global COUNT
#     COUNT = COUNT+1
