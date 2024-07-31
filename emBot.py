import telegram
import asyncio
import time
import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
load_dotenv()

TOKEN= os.getenv('TOKEN')
BOT_USERNAME = os.getenv('BOT_USERNAME')

bot = telegram.Bot(token=TOKEN)
chat = "6314825879"
deny = "691646481"

class botControl:
    
    async def send_message(self, text, chat_id):
        async with bot:
            await bot.send_message(text=text, chat_id=chat_id)

    async def warning(self, room):  
        with open('test.txt', 'r+') as file:
            lines = file.readlines()
            if "kebakaran" in lines[-1]:
                asyncio.run(self.send_message(f"Emergency! Fire at {room}", chat_id=deny))
            elif 'maling' in lines[-1]:
                asyncio.run(self.send_message(f"Emergency! Break in at {room}", chat_id=chat))
            elif 'sakit' or 'tolong' in lines[-1]:
                asyncio.run(self.send_message(f"Medical Emergency at {room}", chat_id=deny))
            else:
                print("no activity")
    

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = botControl()
    asyncio.ensure_future(app.warning("A20"))
    loop.run_forever()