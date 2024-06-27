import speech_recognition as sr
import pyttsx3 
import pywhatkit
import json

testVoice = sr.AudioFile('audio_python.wav')
recognizer = sr.Recognizer()
microphone = sr.Microphone()

def get_command():
    try:
        with microphone as source:
            victus = False
            micAudio = recognizer.listen(source)
            command = recognizer.recognize_google(micAudio, language = "id-ID")
            return command
    
    except sr.UnknownValueError:
        SpeakText("I do not understand")
        pass
    except sr.WaitTimeoutError:
        SpeakText("No speech detected")
    except Exception as e:
        print("An error occured:", str(e))
    return command

def SpeakText(command):
    #Initialize the engine
    engine = pyttsx3.init()
    engine.say(command) 
    engine.runAndWait()

ready = True

while(ready):
    print("listening")
    command = get_command()
    print(command)
    if 'mainkan' in command:
        song = command.replace('mainkan', '')
        SpeakText(f"playing {song}")
        pywhatkit.playonyt(song)
    
        
    elif 'berhenti' in command:
        ready = False
    
    
   # SpeakText(words)