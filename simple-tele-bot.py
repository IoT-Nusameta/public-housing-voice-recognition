import requests
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

command_txt_path = "test.txt"

token = os.getenv('TOKEN')
chat_id = os.getenv('CHAT_ID')

class App:

    async def read_command(self):
        while True:
            # txt_file = open(command_txt_path, "r+")
            # read_str = txt_file.readlines().lower()
            with open('test.txt', 'r+') as file:
                lines = file.readlines()
            print(lines[-1])
            
            if "kebakaran" in lines[-1]:
                msg = "Emergency! Fire at room A4"

                url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg}"
                print(requests.get(url).json())
            elif "maling" or "tolong" in lines[-1]:
                msg = "Emergency! Maling at room A4"

                url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg}"
                print(requests.get(url).json())
            else:
                print("no activity")

            await asyncio.sleep(1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = App()
    asyncio.ensure_future(app.read_command())
    loop.run_forever()