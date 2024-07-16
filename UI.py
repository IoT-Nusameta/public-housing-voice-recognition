from nicegui import ui
import pyttsx3

txt_path = 'test.txt'
my_name = 'apple'
engine = pyttsx3.init()
old_str_file = ''

def read_text():
    global old_str_file

    txt_file = open(txt_path, "r+")
    str_file = txt_file.read()
    print(str_file.lower())
    if old_str_file != str_file:
        if str_file.lower().find(my_name) != -1:
            engine.say("Yes")
            engine.runAndWait()
    
    old_str_file = str_file

ui.timer(1.0, lambda: read_text())

ui.run()