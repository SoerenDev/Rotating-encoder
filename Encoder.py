import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect

client.connect("10.42.0.244", 1883, 60)

client.loop_start()


GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN)
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)

value_left = 0
value_right = 0
value_state = 0
position_value = 0
lastState = 0
ledState = 0 

while True:
    
    if GPIO.input(18) and not GPIO.input(17) and value_left:
        position_value +=1
        value_left = 0
        print(position_value)

    elif not GPIO.input(18) and GPIO.input(17) and value_right:
        position_value -= 1
        print(position_value)

    value_right = not GPIO.input(18) and not GPIO.input(17)
    value_left = not GPIO.input(18) and not GPIO.input(17)

    if position_value%30 == 0 and position_value != 0 and value_state: 
        client.publish("foobar/oben/lounge/beamer/action", "hdmi1")
        print("hdmi1")
        value_state = 0
    
    elif position_value%20 == 0 and position_value != 0 and value_state:
        client.publish("foobar/oben/lounge/beamer/action", "hdmi2")
        print("hdmi2")
        value_state = 0
    
    elif position_value%10 == 0 and position_value != 0 and value_state:
        client.publish("foobar/oben/lounge/beamer/action", "vga")
        print("vga")
        value_state = 0
    
    elif not value_state and position_value%10 != 0:
        value_state = 1
     
    #Taster

    if not GPIO.input(27) != lastState:
    
        if not GPIO.input(27):
    
                if ledState:
                        ledState = 0
                        client.publish("foobar/oben/lounge/beamer/action", "off")
                        print("Aus")
    
                else:
                        ledState = 1
                        client.publish("foobar/oben/lounge/beamer/action", "on")
                        print("An")
    
        lastState = not GPIO.input(27)
