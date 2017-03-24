# mqtt_monitor

Provides a daemon to check on a mqtt broker by sending scheduled messages and execute shell commands depending on the broker reply. The idea is to monitor different apps or devices that comunicate via MQTT protocol. It is developed primarly for monitoring several services on raspberry Pi's in a Home Automation network, but can be used for any kind of MQTT monitoring.

# Stage
The software is really in alpha level, so use it with caution.

# Setup

Create yaml file named "settings.yaml" and define connection details:

```yaml

server:
 ip: MQTTIP
 port: PORT
 username: USER
 password: PASS


```

Rules are implemented in two ways, incoming and outgoing. Incoming are rules that react when a topic is specified:


```yaml

rules:
- incoming:
   expect: monitor/controller/ok
   on_message: echo "controller is working"
   send: monitor/controller/checked

```

    - expect: a topic that the broker may send
    - on_message: a shell command that is executed
    - send: a topic to publish back when the first message is arrived
    
Either on_message or send or both should be specified, otherwise it does not do anything.

Outgoing rules inquire the broker and react to it:

```yaml

rules:
- outgoing:
   send: monitor/controller/status
   expect: monitor/controller/ok
   interval:
    seconds: 600
   on_message: echo "monitoring robot fine"
   timeout: 5
   on_timeout: server controller restart

```

    - send: a topic to publish to inquire the broker
    - expect: a topic that the broker should send back
    - on_message: a shell command that is executed if the expect topic is returned by the broker
    - on_timeout: a shell command that is executed if the broker does not reply
    - timeout: seconds to wait for the borker reply
    - interval: interval in seconds between each inquiring. Can be seconds, minutes, hours, days, weeks. 
    





# Usage

```bash
monitor /path/to/setting/

```

Specify only the folder that contains the settings.yaml file

# Init

Use the file in the init folder to lauch monitor at boot time with systemd or init.d
