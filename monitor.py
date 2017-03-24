#!/usr/bin/python3
import sys
import random
import subprocess
import paho.mqtt.client as mqtt
from mqconnect import Mqconnect
from conf import Conf
from scheduler import Scheduler
from pprint import pprint
import datetime

class Mqmonitor:
    def __init__(self,path):
       conf=Conf(path)
       sets=conf.getValue("settings","server")
       self.mqconnect=Mqconnect(sets['ip'],sets['port'])
       if "username" in sets:
         self.mqconnect.client.username_pw_set(sets['username'],sets['password'])
       mqtt_options=conf.getValue("settings","mqtt")
       if "topic" in mqtt_options:
         self.mqconnect.topic=mqtt_options['topic']
      


       self.rules=conf.getValue("settings","rules")
       self.incoming=self.getActions("incoming")
       self.outgoing=self.getActions("outgoing")
       self.incoming=self.incoming+self.outgoing
       self.sched=Scheduler()
       self.sched.setJob(self.job)
       for rule in self.outgoing:
         self.sched.dispatch(rule)  

    def getActions(self,what):
      actions=[]
      for  k in self.rules:
          if what in k:
             new=k[what]
             new['id']=str(random.randint(1, 10000000000000))
             actions.append(k[what])
      return(actions)

    def execute_shell(self,command):
       output = subprocess.check_output(command,shell=True)
       print(output)

    def on_message(self,client, userdata, msg):
       for k in self.incoming:
          if k['expect']==str(msg.topic):
            print("received message %s" % str(msg.topic))
            self.execute_shell(k['on_message'])
            if "on_timeout" in k:
              self.sched.scheduler.remove_job(k['id']+"on_timeout")

    def start(self):
       self.mqconnect.client.on_message=self.on_message
       self.mqconnect.start()

    def job(self,rule):
      if "on_timeout" in rule:
          when=datetime.datetime.now()
          when=when+datetime.timedelta(seconds=rule['timeout'])
          print("rule %s trigger at %s if timeout" % (rule['on_timeout'], when))
          print("rule untrigger by %s wihin %s" % (rule['expect'], rule['timeout']))

          id=rule['id']+"on_timeout"
          self.sched.scheduler.add_job(self.execute_shell,trigger='date',run_date=when,args=[rule['on_timeout']],id=id,replace_existing=True)
      if "send" in rule:
          self.mqconnect.send(rule['send'])
   
if __name__ == "__main__":
       mqm=Mqmonitor(sys.argv[1])
       mqm.start()

