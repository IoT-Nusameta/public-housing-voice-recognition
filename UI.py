from nicegui import app, ui
import speech_recognition as sr

recognizer = sr.Recognizer()
microphone = sr.Microphone()


def get_command():
    try:
        with microphone as source:
            micAudio = recognizer.listen(source)
            command = recognizer.recognize_google(micAudio)
    except sr.UnknownValueError:
        command = "I do not understand"
    except sr.WaitTimeoutError:
        command = "No speech detected"
    except Exception as e:
        command = "An error occured"
    return command



@ui.refreshable
def check_txt(data):
    speechLog = ui.log(max_lines=100).classes('w-full h-60')
    speechLog.push(data)
            

ui.label("Smart home app")
  

with ui.row():
    ui.button(text="turn on light 1")
    ui.button(text="turn on light 2")
    ui.button(text="turn on light 3")
with open('test.txt', 'r+') as file:
    data = file.read()
check_txt(data)
ui.timer(1, lambda: check_txt.refresh(data))

ui.run()