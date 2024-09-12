from nicegui import ui
from gpiozero import LED
import asyncio

# Setup GPIO pin 17 for controlling an LED

async def turn_on_led():
    LED(4).on()
    await asyncio.sleep(1)  # Keep the LED on for 1 second
    print("hello")
    LED(4).off()

async def turn_off_led():
    LED(4).off()

# Define UI

ui.label('Control LED on GPIO pin 17')

ui.button('Turn LED On', on_click=lambda: asyncio.create_task(turn_on_led()))
ui.button('Turn LED Off', on_click=lambda: asyncio.create_task(turn_off_led()))

ui.run()
