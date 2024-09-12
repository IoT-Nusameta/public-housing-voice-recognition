from gpiozero import LED, CPUTemperature
from time import sleep
from signal import pause

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

def chip_temp():
    cpu = CPUTemperature()
    # print(cpu.temperature)
    return cpu.temperature

def state_relay(pin_index, state):
    relay = define_relay(pin_index)
    relay.on() if state == True else relay.off()
    # pause()
    # exit()

# relay = define_relay(1)
# while True:
#     relay.on()
#     sleep(2)
#     relay.off()
#     sleep(2)


# state_relay(1, False)

print(chip_temp())
toggle_relay(1)
# toggle_all_relay()
# print("finish")