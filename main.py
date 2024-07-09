import speech_recognition as sr
import pyttsx3 
import pywhatkit
import json

testVoice = sr.AudioFile('audio_python.wav')
recognizer = sr.Recognizer()
microphone = sr.Microphone()

with open("dict.json") as thfile:
    data = json.load(thfile)


def get_command():
    try:
        with microphone as source:
            SpeakText("I am online")
            micAudio = recognizer.listen(source)
            command = recognizer.recognize_google(micAudio, language = "id-ID")
            if 'ikaris' in command:
                command = command.replace('ikaris', '')
                print(command)
    
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

def getSynonym(word):
    if word in data.keys():
        return data[word]["sinonim"]
    else:
        pass

listening = True

while(listening):
    print("listening")
    command = get_command()
    #if "mainkan" or getSynonym("mainkan") in command.lower():
    #    song = command.replace('mainkan', '')
    #    SpeakText(f"playing {song}")
    #    pywhatkit.playonyt(song)

    if ("nyala" and "lampu") or (getSynonym("nyala") and getSynonym("lampu")) in command.lower():
        SpeakText("Turning on the lights")             
                    
    elif 'berhenti' in command.lower():
        listening = False
        
        
   # SpeakText(words)