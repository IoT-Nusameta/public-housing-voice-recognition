from nicegui import app, ui
# import speech_recognition as sr


data = {"alcon": "marmut", 'test': 'pisang'}

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


@ui.refreshable
def check_txt(data):
    speechLog = ui.log(max_lines=100).classes('w-full h-60')
    speechLog.push(data)

@ui.page('/login')
def login():    
    def check_pass():
        if data.get(username.value) == password.value:
            ui.notify("Correct password!")
            ui.navigate.to('await')
        else:
            ui.notify("something is not right")

    with ui.card().classes('absolute-center'):
        username = ui.input('Username')
        password = ui.input('Password', password=True, password_toggle_button=True)
        ui.button('Log in', on_click=check_pass)

@ui.page('/await')
def static_mode():
    ui.label('Awaiting voice activation')
    with open('test.txt', 'r') as file:
        data = file.read()
@ui.page('/main_content')
def main_content():

    with ui.card(align_items='center').classes('absolute-center'):
        ui.label("Smart home app")
        with ui.row():
            ui.button(text="turn on light 1")
            ui.button(text="turn on light 2")
            ui.button(text="turn on light 3")
        with open('test.txt', 'r+') as file:
            data = file.read()
        check_txt(data)
        ui.timer(4, lambda: check_txt.refresh(data))

login()
ui.run()