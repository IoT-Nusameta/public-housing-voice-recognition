import speech_recognition as sr
import pyttsx3 
import pywhatkit as wa
import json
import asyncio
from nicegui import app, ui

recognizer = sr.Recognizer()
microphone = sr.Microphone()

light_on = False
def get_command():
    try:
        with microphone as source:
            micAudio = recognizer.listen(source, 5)
            command = recognizer.recognize_google(micAudio, language = "id-ID")
            if 'ikaris' in command:
                command = command
    except sr.UnknownValueError:
        SpeakText("I do not understand")
        command = 'say it again'
    except sr.WaitTimeoutError:
        SpeakText("No speech detected")
        command = "say it again"
    except Exception as e:
        print("An error occured:", str(e))
        command = 'say it again'
    return command

def SpeakText(command):
    #Initialize the engine
    engine = pyttsx3.init()
    engine.say(command) 
    engine.runAndWait()


async def hear():
    await get_command()

listening = True


while(listening):
    print("listening")
    command = get_command()

    with open('test.txt', 'a+') as file:
        if not command == 'say it again':
            file.writelines(f"\n{command}")
    
    if "mainkan" in command.lower():
        song = command.replace('mainkan', '')
        SpeakText(f"playing {song}")
        wa.playonyt(song)

    # elif ("nyala" or "matikan") and "lampu" in command.lower():
    #     if light_on == False:
    #         SpeakText("Turning on the lights If there is any")
    #         UI.check_txt.refresh("Turning on the lights...If there is any")
    #         light_on == True
    #     elif light_on == True:
    #         SpeakText("Turning off the lights If there is any")
    #         UI.check_txt.refresh("Turning off the lights...If there is any")           
    #         light_on == False        
    elif 'keluar' in command.lower():
        SpeakText("Exiting")
        listening = False
        
    elif 'tolong' in command.lower():
        SpeakText("calling for help")

    else:
        print(command)
        
        
  #Dear stranger who is reading this, I am having trouble with this code, if you could help in any way it would be appreciated.
