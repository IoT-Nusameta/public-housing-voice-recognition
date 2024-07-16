from whisper_mic import WhisperMic

while True:
    txt_file = open("test.txt","w")
    mic = WhisperMic()
    result = mic.listen()
    print(result)
    
    txt_file.write(result)