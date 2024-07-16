import speech_recognition as sr

recognizer = sr.Recognizer()
microphone = sr.Microphone()

def get_command():
    try:
        with microphone as source:
            micAudio = recognizer.listen(source, 5)
            command = recognizer.recognize_google(micAudio, language = "id-ID")
    except Exception as e:
        print("An error occured:", str(e))
        command = 'say it again'
    return command

while True:
    txt_file = open("test.txt","w")
    
    print('listening ...')
    command = get_command()
    print(command)

    txt_file.write(command)