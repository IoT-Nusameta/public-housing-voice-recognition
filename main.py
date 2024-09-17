import multiprocessing
multiprocessing.set_start_method("spawn", force=True)
from nicegui import ui,app
import os
from datetime import datetime
from dateutil import tz
from dotenv import load_dotenv
from process.json_interface import *
from process.influxdb_interface import *
import subprocess
import plotly.graph_objects as go
from random import random

load_dotenv()

parent_path = os.getenv('PARENT_PATH')
voice_path = parent_path + '/temp/voice.txt'
src_lottie_listen = parent_path + '/assets/listen.json'
src_lottie_lock = parent_path + '/assets/locked.json'

app.native.window_args['resizable'] = False
app.native.start_args['debug'] = False
app.native.settings['ALLOW_DOWNLOADS'] = True
app.add_static_files(parent_path, parent_path)
old_read_str = ''

def read_txt(current_page):
    global old_read_str, log
    now = datetime.now().strftime('%H:%M:%S')

    txt_file = open(voice_path, "r+")
    read_str = txt_file.read().lower()
    if old_read_str != read_str:
        print(read_str)
        if current_page == 'listen_page':
            words = read_str.split(':')
            log.push(f'[{now}]: {words[1]}')

    if current_page == 'lock_page':
        if 'buka' in read_str:
            ui.navigate.to(listen_page)
    elif current_page == 'listen_page':
        if 'tutup' in read_str:
            ui.navigate.to(lock_page)
        
    old_read_str = read_str

@ui.page('/lock_page')
def lock_page():    
    ui.timer(1.0, lambda: read_txt('lock_page'))

    ui.row().classes('h-40')
    ui.add_body_html('<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>')
    with ui.row().classes('grid grid-cols-12 w-full gap-4'):
        ui.html(f'<lottie-player src="{src_lottie_lock}" loop autoplay />').classes('col-start-2 col-span-10 h-30')
    
    with ui.page_sticky(x_offset=18, y_offset=18):
        ui.button(icon='key', on_click=lambda:ui.navigate.to(listen_page)).props('fab color=green-5')

@ui.page('/listen_page')
def listen_page():
    global log

    ui.timer(1.0, lambda: read_txt('listen_page'))

    def empty_func(number, state):
        print(f"something{str(number)}: {state}")
        # button_bedroom.props('color=blue')

    # def toggle_relay(relay, state):


    class ToggleButton(ui.button):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            # self._state = False
            if self._props['label'] == 'Bedroom':
                self._state = read_relay('relay1')
                # if self._state == True:
                #     self._props['color'] = 'green'
                # else:
                #     self._props['color'] = 'red'
            elif self._props['label'] == 'Kitchen':
                self._state = read_relay('relay2')
            elif self._props['label'] == 'Backyard':
                self._state = read_relay('relay3')
            elif self._props['label'] == 'Street':
                self._state = read_relay('relay4')
            self.on('click', self.toggle)
        def toggle(self) -> None:
            """Toggle the button state."""
            self._state = not self._state
            self.update()
        def update(self) -> None:
            self.props(f'color={"green" if self._state else "red"}')
            if self._props['label'] == 'Bedroom':
                # empty_func(1, self._state)
                make_state_relay('relay1', self._state)
            elif self._props['label'] == 'Kitchen':
                # empty_func(2, self._state)
                make_state_relay('relay2', self._state)
            elif self._props['label'] == 'Backyard':
                # empty_func(3, self._state)
                make_state_relay('relay3', self._state)
            elif self._props['label'] == 'Street':
                # empty_func(4, self._state)
                make_state_relay('relay4', self._state)
            super().update()

    with ui.page_sticky(position='top',x_offset=18, y_offset=18):
        ui.add_body_html('<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>')
        with ui.row().classes('grid grid-cols-12 w-full gap-4'):
            ui.html(f'<lottie-player src="{src_lottie_listen}" loop autoplay />').classes('col-start-2 col-span-10 h-30')

    ui.row().classes('h-80')
    with ui.row().classes('grid grid-cols-10 w-full gap-4'):
        # button_bedroom = ToggleButton('Bedroom').classes('col-start-2 col-span-2 h-10').props('fab')
        ToggleButton('Bedroom').classes('col-start-2 col-span-2 h-10').props('fab')
        ToggleButton('Kitchen').classes('col-start-4 col-span-2 h-10').props('fab')
        ToggleButton('Backyard').classes('col-start-6 col-span-2 h-10').props('fab')
        ToggleButton('Street').classes('col-start-8 col-span-2 h-10').props('fab')

    log = ui.log(max_lines=20).classes('w-full h-100')

    with ui.page_sticky(x_offset=18, y_offset=18):
        ui.button(icon='lock', on_click=lambda:ui.navigate.to(lock_page)).props('fab color=red-5')
    with ui.page_sticky(x_offset=18, y_offset=18, position='bottom-left'):
        ui.button(icon='solar_power', on_click=lambda:ui.navigate.to(chart_page)).props('fab color=orange-5')
    

@ui.page('/chart_page')
def chart_page():
    ui.row().classes('h-40')
    fig = go.Figure()
    fig.update_layout(height=400,margin=dict(l=0, r=0, t=0, b=0))
    plot = ui.plotly(fig).classes('w-full h-40')

    def update_trace():
        timestamp, voltage_data, current_data = query_power()

        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        local_timestamp = []

        for i in timestamp:
            str_utc = i.split('.')[0]
            naive = datetime.strptime(str_utc, "%Y-%m-%dT%H:%M:%S")
            utc = naive.replace(tzinfo=from_zone)
            local = utc.astimezone(to_zone)
            local_timestamp.append((local))
        
        my_dict = {
            'data': [
                {
                    'type': 'scatter',
                    'name': 'v_plot (mV)',
                    'x': local_timestamp,
                    'y': voltage_data,
                    'line': {'width': 2},
                },
                {
                    'type': 'scatter',
                    'name': 'i_plot (mA)',
                    'x': local_timestamp,
                    'y': current_data,
                    'line': {'dash': 'dot', 'width': 2},
                },
            ],
            'layout': {
                'legend': {
                    'yanchor': "top",
                    'y': 0.99,
                    'xanchor': "left",
                    'x': 0.01
                }
            }
        }
        fig.update(my_dict)
        plot.update()

    ui.timer(1.0, lambda:update_trace())

    with ui.page_sticky(x_offset=18, y_offset=18):
        ui.button(icon='lock', on_click=lambda:ui.navigate.to(lock_page)).props('fab color=red-5')
    

# subprocess.Popen(["/home/photobooth/public-housing-voice-recognition/.venv/bin/python", "/home/photobooth/public-housing-voice-recognition/process/speech_online.py"])
# subprocess.Popen(["/home/photobooth/public-housing-voice-recognition/.venv/bin/python", "/home/photobooth/public-housing-voice-recognition/process/aio-serial.py"])
# subprocess.Popen(["/home/photobooth/public-housing-voice-recognition/.venv/bin/python", "/home/photobooth/public-housing-voice-recognition/process/telebot.py"])

lock_page()

ui.run(native=True, window_size=(480, 800), fullscreen=True ,frameless=False)
# ui.run()