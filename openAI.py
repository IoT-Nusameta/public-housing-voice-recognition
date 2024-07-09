import openai
from whisper_mic import WhisperMic

openai.api_key = 'sk-proj-q3TE7xshu3IVDx7rgmHIT3BlbkFJNA8jcruqtcYu4BpXXB2t'

mic = WhisperMic()
result = mic.listen()
print(result)