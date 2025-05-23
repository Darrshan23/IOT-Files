import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("connected with result code"+str(rc))
    client.subscribe("/edge_device/data")

def on_message(client, userdata, msg):
    print(msg.topic+""+str(msg.payload))
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.56.111", 1883,60)

client.loop_forever()