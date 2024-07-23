import speech_recognition as sr
import pyttsx3 
import pywhatkit
import json
from nicegui import app, ui

recognizer = sr.Recognizer()
microphone = sr.Microphone()

with open("dict.json") as thfile:
    data = json.load(thfile)


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

def getSynonym(word):
    if word in data.keys():
        return data[word]["sinonim"]
    else:
        pass

listening = True


while(listening):
    print("listening")
    command = get_command()

    with open('test.txt', 'w') as file:
        file.writelines(f"\n{command}")
    
    if "mainkan" in command.lower():
        song = command.replace('mainkan', '')
        SpeakText(f"playing {song}")
        pywhatkit.playonyt(song)

    elif "nyala" and "lampu" in command.lower():
        SpeakText("Turning on the lights")             
                    
    elif 'keluar' in command.lower():
        SpeakText("Exiting")
        listening = False
    
    else:
        print(command)
        
        
  #Dear stranger who is reading this, I am having trouble with this code, if you could help in any way it would be appreciated.
