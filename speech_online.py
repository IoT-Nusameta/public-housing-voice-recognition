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
    print('listening ...')
    command = get_command()
    
    with open('test.txt', 'w') as file:
        file.writelines(f"{command}")
    
    print(command)

    # run both this .py and gui.py
    # login page is loaded
    # try to say "hey ikaris", whatever including "ikaris"
    # from login page navitaged to test page
    # try yo say "tutup aplikasi", whatever including tutup
