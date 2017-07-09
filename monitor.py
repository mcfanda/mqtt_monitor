#!/usr/bin/python3
import sys
import random
import subprocess
import paho.mqtt.client as mqtt
from modules.mqconnect import Mqconnect, cleanmsg
from modules.conf import Conf
from modules.scheduler import Scheduler
from pprint import pprint
import datetime

settings={
    'timeout' : 10
    }

class Mqmonitor:
    def __init__(self,path):
        conf=Conf(path)
        sets=conf.getValue("settings","server")
        self.mqconnect=Mqconnect(sets['ip'],sets['port'])

        if "username" in sets:
                self.mqconnect.client.username_pw_set(sets['username'],sets['password'])
        mqtt_options=conf.getValue("settings","mqtt")

        if mqtt_options and "topic" in mqtt_options:
                self.mqconnect.topic=mqtt_options['topic']

        if mqtt_options and "will" in mqtt_options:
                self.mqconnect.client.will_set(mqtt_options['will'],"lost")

        self.rules=conf.getValue("settings","rules")
        self.incoming=self.getActions("incoming")
        self.outgoing=self.getActions("outgoing")
        self.incoming=self.incoming+self.outgoing
        self.sched=Scheduler()
        self.sched.setJob(self.job)
        for rule in self.outgoing:
                self.sched.dispatch(rule)

    def process(self,action):
        action['id']=str(random.randint(1, 10000000000000))
        if "name" not in action:
            action['name']=action['id']
        if "on_timeout" in action and "timeout" not in action:
            action["timeout"]=settings["timeout"]
        if "reply" in action and "reply_payload" not in action:
            action["reply_payload"]=None
        if "send" in action and "send_payload" not in action:
            action["send_payload"]=None
        if "expect" in action and "expect_payload" not in action:
            action["expect_payload"]=None
        if "reply_on_timeout" in action and "reply_on_timeout_payload" not in action:
            action["reply_on_timeout_payload"]=None

        return(action)

    def getActions(self,what):
        actions=[]
        for  k in self.rules:
            if what in k:
                new=k[what]
                new=self.process(new)
                actions.append(k[what])
        #pprint(actions)
        return(actions)

    def execute_shell(self,command):
        output = subprocess.check_output(command,shell=True)
        print(output)

    def on_message(self,client, userdata, msg):
        for rule in self.incoming:
            if rule['expect']==str(msg.topic):
                if rule["expect_payload"] and rule["expect_payload"]!=cleanmsg(msg.payload):
                    print("message %s with payload %s received but does not match %s " % (str(msg.topic),cleanmsg(msg.payload),rule["expect_payload"]))
                    continue
                print("received message %s" % str(msg.topic))
   
                if "on_message" in rule:
                    self.execute_shell(rule['on_message'])
  
                if "on_timeout" in rule:
                    try:
                        self.sched.scheduler.remove_job(rule['id']+"on_timeout")
                    except:
                        print("not timeout rule present")
                
                if "reply" in rule:
                    self.mqconnect.send(rule['reply'],rule['reply_payload'])

                if "reply_on_timeout" in rule:
                    try:
                        self.sched.scheduler.remove_job(rule['id']+"on_timeout_reply")
                    except:
                        print("not timeout reply present")



    def start(self):
       self.mqconnect.client.on_message=self.on_message
       self.mqconnect.start()

    def job(self,rule):
      if "on_timeout" in rule:
          when=datetime.datetime.now()
          when=when+datetime.timedelta(seconds=rule['timeout'])
          print("action %s trigger at %s if timeout" % (rule['name'], when))
          print("untrigger action by %s within %s" % (rule['expect'], rule['timeout']))
          id=rule['id']+"on_timeout"
          self.sched.scheduler.add_job(self.execute_shell,trigger='date',run_date=when,args=[rule['on_timeout']],id=id,replace_existing=True)
      if "send" in rule:
          self.mqconnect.send(rule['send'],rule['send_payload'])
      if "reply_on_timeout":
          when=datetime.datetime.now()
          when=when+datetime.timedelta(seconds=rule['timeout'])
          id=rule['id']+"on_timeout_reply"
          self.sched.scheduler.add_job(self.mqconnect.send,trigger='date',run_date=when,args=[rule['reply_on_timeout'],rule['reply_on_timeout_payload']],id=id,replace_existing=True) 
 
          
if __name__ == "__main__":
       if len(sys.argv)<2 :
          print("Please specify a setting file folder")
          exit(1)
       mqm=Mqmonitor(sys.argv[1])
       mqm.start()
