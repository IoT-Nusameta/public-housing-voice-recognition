from gpiozero import LED
from time import sleep

pin_array = [4, 22, 6, 26]

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

def toggle_all_relay():
    for i in range(len(pin_array)):
        relay = define_relay(i)
        relay.on()
    sleep(1)
    for i in range(len(pin_array)):
        relay = define_relay(i)
        relay.off()

# toggle_relay(0)
# toggle_all_relay()
# print("finish")