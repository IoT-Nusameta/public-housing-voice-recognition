# import multiprocessing
# multiprocessing.set_start_method("spawn", force=True)
from nicegui import ui,app
import gpiozero
from time import sleep
from signal import pause
# import subprocess
import os


# pin_array = [4, 22, 6, 26]

# def define_relay(pin_index):
#     global pin_array
#     pin = pin_array[pin_index]
#     relay = LED(pin)
#     return relay

# def toggle_relay(pin_index):
#     relay = define_relay(pin_index)
#     relay.on()
#     sleep(1)
#     relay.off()


def init_relay():
    RELAY_PIN = 4
    relay = gpiozero.OutputDevice(RELAY_PIN, active_high=True, initial_value=False)
    relay.on()
    print("saya disini")
    pause()
    # sleep(1)
    # relay.off()
    # return relay

def relay_on():
    relay = init_relay()

ui.label("hallo dunia")

# ui.button('on', on_click=lambda:relay.on())
ui.button('on', on_click=lambda:print(init_relay()))
ui.button('off', on_click=lambda:print("hall"))

ui.run()

# toggle_relay(2)