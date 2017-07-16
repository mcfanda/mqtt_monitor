#!/usr/bin/python3

import paho.mqtt.client as mqtt
from datetime import datetime
from time import sleep
import logging

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
             logging.info("trying connecting to mqtt broker")
             self.client.connect(self.ip, self.port, 60)
             con=True
          except Exception:
             logging.warning("Problem with the connection") 
          sleep(15)   
        logging.info("connection shold be ok")
        self.client.loop_forever()
 
    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
           logging.warning("Mqconnect: Connected to topic %s with result code %s" % (self.topic,str(rc)))
           self.client.subscribe(self.topic)

        else:
             logging.warning("Mqconnect: Connection problems with code %s" % (str(rc)))
             logging.warning("Trying again:")
             sleep(10)
             self.start()
             
    def on_message(self,client, userdata, msg):
        print("Mqconnect: received "+str(msg.topic))

    def on_disconnect(self, client, obj, rc):
        logging.warning("connection to broker is gone. Trying reconnect...")
        con=False
        while (not con):
          try:
             client.reconnect()
             con=True
          except Exception:
             logging.warning("no joy")
          sleep(10)
    
           
    def send(self,topic,msg=None):
       try:
          self.client.publish(topic,msg,retain=False)
       except Exception:
           logging.error("There is a problem in sendinf the message to %s" % topic )





if __name__ == "__main__":
  mq=Mqconnect("127.0.0.1",1883)
  mq.start()
