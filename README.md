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
   reply: monitor/controller/checked
   reply_payload: ciao

```

This rule waits for the broker to publish in the "monitor/controller/ok" topic. When it gets a message execute the shell command in "on_message" key.
 It also reply to the broker in "monitor/controller/checked" topic (reply:) with a payload of "ciao".

 Allowed keys are:

    - expect: a topic that the broker may send
    - expect_payload: optional payload to be received in the expect topic
    - on_message: a shell command that is executed
    - reply: a topic to publish back when the first message is arrived
    - reply_payload: optional payload to publish in the reply topic

Either on_message or reply or both should be specified, otherwise it does not do anything.

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

This rule publishes to "monitor/controller/status" topic (send:) every 600 secs. When the message is published, it waits 5 secs (timeout:)
for the boker to reply in the "monitor/controller/ok" topic. If the broker replies the "on_message:" command is executed in a shell,
otherwise the command in the "on_timeout:" is execute.

Allowed keys are:


    - send: a topic to publish to inquire the broker
    - send_payload: optional paylaod for the send topic
    - expect: a topic that the broker should send back
    - expect_payload: option payload for the expect topic
    - on_message: a shell command that is executed if the expect topic is returned by the broker
    - on_timeout: a shell command that is executed if the broker does not reply
    - reply_on_timeout: a topic to send to if the broker does not reply
    - reply_on_timeout_payload: optional payload for reply on timeout
    - timeout: seconds to wait for the borker reply
    - interval: interval in seconds between each inquiring. Can be seconds, minutes, hours, days, weeks.



Obviously, one can use this module as a shell actuator of MQTT protocol.
Imagine you want to erase a directory on your server whenever the alarm goes off, that is the sensors turn on, you can set a rule like this (silly example, I know):

```yaml

rules:
- incoming:
   expect: house/alarm
   expect_payload: "on"
   on_message: rm -r /path/to/secrets
   reply: house/privacy
   reply_payload: "assured"

```



# Usage

```bash
monitor /path/to/setting/

```

Specify only the folder that contains the settings.yaml file

# Init

Use the file in the init folder to lauch monitor at boot time with systemd or init.d

# Mqtt settings

You can set some defaults for the mqtt connection in the setting.yaml file

```yaml
mqtt:
 will: /monitor/controller/connection

```
    - will: set the topic that will be published if connection is lost. Payload is "lost"
