#!/usr/bin/python3

import paho.mqtt.client as mqtt
from datetime import datetime
from time import sleep

def cleanmsg(bytestring):
           res=str(bytestring)[1:]
           return res.replace("'","")


class Mqconnect:
    def __init__(self,ip,port,username=None,pasw=None):
        self.ip=ip
        self.port=port
        self.client = mqtt.Client()
        self.messages ={}
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.topic="#"

        if username:
             self.client.username_pw_set(username, password=pasw)

    
    def start(self):
        con=False
        while (not con):
          try:
             self.client.connect(self.ip, self.port, 60)
             con=True
          except Exception:
             print("Problem with the connection") 
          sleep(15)   
 
    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
           print("Mqconnect: Connected to topic %s with result code %s" % (self.topic,str(rc)))
           self.client.subscribe(self.topic)
           self.client.loop_forever()

        else:
             print("Mqconnect: Connection problems with code %s" % (self.topic,str(rc)))
             print("Trying again:")
             sleep(10)
             self.start()
             
    def on_message(self,client, userdata, msg):
        print("Mqconnect: received "+str(msg.topic))

    def on_disconnect(self, client, obj, rc):
        print("connection to broker is gone. Trying reconnect...")
        client.reconnect()

    def send(self,topic,msg=None):
       try:
          self.client.publish(topic,msg,retain=False)
       except Exception:
           print("There is a problem in sendinf the message to %s" % topic )





if __name__ == "__main__":
  mq=Mqconnect("127.0.0.1",1883)
  mq.start()
