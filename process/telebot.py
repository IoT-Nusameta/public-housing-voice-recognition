import requests
# import asyncio
import time
import os
from dotenv import load_dotenv

load_dotenv()
parent_path = os.getenv('PARENT_PATH')
voice_path = parent_path + '/temp/voice.txt'
human_path = parent_path + '/temp/human.txt'

token = os.getenv('TELEBOT_TOKEN')
personal_chat_ids = ["691646481"]
group_chat_ids = ["-4594185135"]

user = "Ikaris"
alamat = "Tower Sequis Lt.9, SCBD, Jakarta"
keywords = ['kebakaran', 'maling', 'tolong', 'polisi', 'pencurian']

def listen_voice():
    txt_file = open(voice_path, "r+")
    read_str = txt_file.read().lower()

    for i in keywords:
        if i in read_str:
            return i
    return False

def watch_distance_sensor():
    txt_file = open(human_path, "r+")
    read_str = txt_file.read().lower()

    if read_str == 'true':
        return True
    else:
        return False

while True:
    try:
        voice = listen_voice()
        if voice != False:
            for i in group_chat_ids:
                msg = "--- Emergency Broadcasting ---\n\n"
                msg += f"Laporan dari {user} yang beralamat di {alamat}.\n\n"
                msg += f"Pesan: {voice.upper()}"

                url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={i}&text={msg}"
                print(requests.get(url).json())

        human_exist = watch_distance_sensor()
        if human_exist == True:
            for i in personal_chat_ids:
                msg = "--- Alarm Triggerd ---\n\n"
                msg += f"Halaman belakang rumah dilintasi seseorang"

                url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={i}&text={msg}"
                print(requests.get(url).json())

        time.sleep(1)
    except Exception as e:
        print("The error is: ", e)