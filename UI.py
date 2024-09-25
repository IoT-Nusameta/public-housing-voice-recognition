from nicegui import app, ui
import datetime 
import json
# import speech_recognition as sr


data = {"alcon": "marmut", 'test': 'pisang'}

prev = ""
# def get_command():
    # try:
        # with microphone as source:
            # micAudio = recognizer.listen(source)
            # command = recognizer.recognize_google(micAudio)
    # except sr.UnknownValueError:
        # command = "I do not understand"
    # except sr.WaitTimeoutError:
        # command = "No speech detected"
    # except Exception as e:
        # command = "An error occured"
    # return command

class ToggleButton1(ui.button):

    def __init__(self, name, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._state = False
        self.name = name
        self.on('click', self.toggle)

    def toggle(self) -> None:
        """Toggle the button state."""
        self.last_state = self._state
        self._state = not self._state
        self.update()

    def update(self) -> None:
        self.props(f'color={"green" if self._state else "red"}')
        # self.light_switch("relay1")
        if self._state:
            self.light_switch(self.name, 1)
        else:
            self.light_switch(self.name, 0)
        # print(self._state)
        super().update()

    def light_switch(self, myKey, state):
        relay_data = load_json()
        relay_data[myKey] = state
        with open("light.json", 'w') as jsonFile:
            json.dump(relay_data, jsonFile)
    
    def check_switch(self, myKey):
        with open("light.json", "r+") as json_data:
            relays = json.load(json_data)
            print(f"state_relay1 = {relays["relay1"]}")
            print(self._props["label"])
            print(self._props)
            if relays[myKey] == 1:
                self._props['color'] = "green"
                super().update()
            else:
                self._props['color'] = "red"
                super().update()
            # print(relays["relay2"])
            # print(relays["relay3"])
        # with open("test.txt", 'r') as openfile:
        #     txt = openfile.readlines()
        #     if "nyalakan" and light in txt[-1]:
        #         self.toggle()
        #     else:
        #         pass

def load_json():
    with open("light.json", 'r') as openfile:
        json_object = json.load(openfile)
        return json_object

def init_light():
    relay_data = load_json()
    for i in relay_data:
        relay_data[i] = 0
    with open("light.json", 'w') as jsonFile:
        json.dump(relay_data, jsonFile)
    print(relay_data)
# def light_switch(myKey):
#     relay_data = load_json()
#     print(relay_data)
#     if relay_data[myKey] == 0:
#         relay_data[myKey] = 1
#         with open("light.json", 'w') as jsonFile:
#             json.dump(relay_data, jsonFile)
#     else:
#         relay_data[myKey] = 0
#         with open("light.json", 'w') as jsonFile:
#             json.dump(relay_data, jsonFile)

def page_check(current_page):
    with open('test.txt', 'r') as file:
        txt = file.readlines()
    if current_page == 'await':
        if "ikaris" in txt[-1]:
            ui.navigate.to('/main_content')
    elif current_page == 'main':
        if "keluar" in txt[-1]:
            ui.navigate.to('/await')

def try_log(log):
    global prev
    current_hour = datetime.datetime.now().hour
    current_minutes = datetime.datetime.now().minute
    current_seconds = datetime.datetime.now().second
    timestamp = f"{current_hour}:{current_minutes}:{current_seconds}"
    with open('test.txt', 'r') as file:
        txt = file.readlines()
    if prev != txt[-1]:
        print(txt[-1])
        log.push(f"{timestamp} {txt[-1]}")
    prev = txt[-1]

@ui.page('/login')
def login():    
    def check_pass():
        if data.get(username.value) == password.value:
            ui.notify("Correct password!")
            ui.navigate.to(static_mode)
        else:
            ui.notify("something is not right")

    with ui.card().classes('absolute-center'):
        username = ui.input('Username')
        password = ui.input('Password', password=True, password_toggle_button=True)
        ui.button('Log in', on_click=check_pass)
    ui.timer(1, lambda: page_check('login'))

@ui.page('/await')
def static_mode():
    ui.label('Awaiting voice activation')
    with open('test.txt', 'r') as file:
        data = file.readlines()
    ui.timer(1, lambda: page_check('await'))
   


@ui.page('/main_content')
def main_content():
    init_light()
    if "ikaris" or "gitaris" in data:
        with ui.card(align_items='center').classes('absolute-center'):
            ui.label("Smart home app")
            with ui.row():
                lampuTeras= ToggleButton1("relay1", "light 1")
                lampuGarasi= ToggleButton1("relay2", "light 2")
                lampuHalaman= ToggleButton1("relay3", "light 3")
                speechLog = ui.log(max_lines=100).classes('w-full h-60')
                # ui.timer(1, lambda: read_txt(data))
                # ui.timer(4, lambda: check_txt(speechLog, data[-1]))
                ui.timer(1, lambda: lampuTeras.check_switch("relay1"))
                ui.timer(1, lambda: lampuGarasi.check_switch("relay2"))
                ui.timer(1, lambda: lampuHalaman.check_switch("relay3"))
                ui.timer(1, lambda: page_check('main'))
                ui.timer(4, lambda: try_log(speechLog))
                
    else:
        ui.label("Waiting....")
login()
ui.run()