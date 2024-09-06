import os
import speech_recognition as sr
from dotenv import load_dotenv
load_dotenv()

parent_path = os.getenv('PARENT_PATH')
voice_path = parent_path + '/temp/voice.txt'

recognizer = sr.Recognizer()
microphone = sr.Microphone()

cycle = 0

def get_command():
    try:
        with microphone as source:
            # micAudio = recognizer.listen(source, 5)
            micAudio = recognizer.listen(source=source, timeout=3, phrase_time_limit=3)
            command = recognizer.recognize_google(micAudio, language = "id-ID")
    except Exception as e:
        print(e)
        command = 'I am listening now ...'
    return command

while True:
    cycle += 1
    command = get_command()    
    padded_cycle = str(cycle).rjust(5, '0')

    with open(voice_path, 'w') as file:
        # file.writelines(command)
        file.writelines(f"[{padded_cycle}]:{command}")

    print(f"[{padded_cycle}]:{command}")

    # run both this .py and gui.py
    # login page is loaded
    # try to say "hey ikaris", whatever including "ikaris"
    # from login page navitaged to test page
    # try yo say "tutup aplikasi", whatever including tutup
