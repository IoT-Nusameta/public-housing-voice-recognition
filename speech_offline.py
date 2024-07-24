from whisper_mic import WhisperMic

mic = WhisperMic()
while True:
    txt_file = open("test.txt","w")
    result = mic.listen()
    print(result)
    
    txt_file.write(result)