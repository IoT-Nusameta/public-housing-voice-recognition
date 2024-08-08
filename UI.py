from nicegui import app, ui
import datetime 
# import speech_recognition as sr


data = {"alcon": "marmut", 'test': 'pisang'}
light1 = False
light2 = False
light3 = False

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
        data = file.read()
    ui.timer(1, lambda: page_check('await'))
   


@ui.page('/main_content')
def main_content():
    if "ikaris" or "Icarus" in data:
        with ui.card(align_items='center').classes('absolute-center'):
            ui.label("Smart home app")
            with ui.row():
                ui.button(text="turn on light 1", on_click=lambda: try_log(speechLog, "Hypothethically turning on light 1...cause it doesnt exist"))
                ui.button(text="turn on light 2", on_click=lambda: try_log(speechLog, "Turning on light 2...in theory"))
                ui.button(text="turn on light 3", on_click=lambda: try_log(speechLog, "Turning on light 3...when there is one"))
                speechLog = ui.log(max_lines=100).classes('w-full h-60')
                # ui.timer(1, lambda: read_txt(data))
                # ui.timer(4, lambda: check_txt(speechLog, data[-1]))
                ui.timer(1, lambda: page_check('main'))
                ui.timer(4, lambda: try_log(speechLog))
                
    else:
        ui.label("Waiting....")
    

login()
ui.run()