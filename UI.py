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
ui.label("Smart home app")
speechLog = ui.log(max_lines=100).classes('w-full h-60')

command = get_command()

ui.button("push to talk", on_click=lambda: speechLog.push(command))

ui.run()