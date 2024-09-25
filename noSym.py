import speech_recognition as sr
import pyttsx3 
import pywhatkit as wa
import json
import asyncio

recognizer = sr.Recognizer()
microphone = sr.Microphone()

light_on = False
def get_command():
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            micAudio = recognizer.listen(source, 5)
            command = recognizer.recognize_google(micAudio, language = "id-ID")
            if 'ikaris' in command:
                command = command
    except sr.UnknownValueError:
        # SpeakText("I do not understand")
        command = 'say it again'
    except sr.WaitTimeoutError:
        # SpeakText("No speech detected")
        command = "say it again"
    except Exception as e:
        print("An error occured:", str(e))
        command = 'say it again'
    return command

# def SpeakText(command):
#     #Initialize the engine
#     engine = pyttsx3.init()
#     engine.say(command) 
#     engine.runAndWait()

def load_json():
    with open("light.json", 'r') as openfile:
        json_object = json.load(openfile)
        return json_object

def query_light(relay):
    tmp = load_json()
    tmp_state = tmp[relay]
    if tmp_state == 1:    
        light_switch(relay, 0)
    else:
        light_switch(relay, 1)

def light_switch(myKey, state):
    relay_data = load_json()
    relay_data[myKey] = state
    with open("light.json", 'w') as jsonFile:
        json.dump(relay_data, jsonFile)

async def hear():
    await get_command()

listening = True


while(listening):
    print("listening")
    command = get_command()
    print(command)
    with open('test.txt', 'a+') as file:
        if not command == 'say it again':
            file.writelines(f"\n{command}")
      
    if "mainkan" in command.lower():
        song = command.replace('mainkan', '')
        # SpeakText(f"playing {song}")
        wa.playonyt(song)

    elif ("nyala" or "matikan") in command.lower():
        if "teras" in command.lower():
            
            query_light("relay1")
        
        elif "kamar" in command.lower():
            query_light("relay2")
   
        elif "halaman" in command.lower():
            query_light("relay3")
     

    # elif 'keluar' in command.lower():
    #     # SpeakText("Exiting")
    #     listening = False
        
    # elif 'tolong' in command.lower():
    #     # SpeakText("calling for help")

    else:
        print("No commands")
        
        
  #Dear stranger who is reading this, I am having trouble with this code, if you could help in any way it would be appreciated.
