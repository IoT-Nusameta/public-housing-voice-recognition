import os
import json
from time import sleep
from signal import pause
from dotenv import load_dotenv
from gpiozero import LED, CPUTemperature

load_dotenv()
parent_path = os.getenv('PARENT_PATH')
relay_path = parent_path + '/temp/relay.json'

pin_array = [4, 22, 6, 26]

def load_json():
    with open(relay_path, 'r') as openfile:
        json_object = json.load(openfile)
        return json_object

def read_relay(relay):
    loaded_data = load_json()
    state = loaded_data[f'{relay}']
    return state

def define_relay(pin_index):
    global pin_array
    pin = pin_array[pin_index]
    relay = LED(pin)
    return relay

def toggle_relay(pin_index):
    relay = define_relay(pin_index)
    relay.on()
    sleep(1)
    relay.off()

relay1 = define_relay(0)
relay2 = define_relay(1)
relay3 = define_relay(2)
relay4 = define_relay(3)

while True:
    relay1.on() if read_relay('relay1') == True else relay1.off()
    relay2.on() if read_relay('relay2') == True else relay2.off()
    relay3.on() if read_relay('relay3') == True else relay3.off()
    relay4.on() if read_relay('relay4') == True else relay4.off()

    sleep(1)
