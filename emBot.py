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

async def send_message(text, chat_id):
    async with bot:
        await bot.send_message(text=text, chat_id=chat_id)

async def main():

    while True:    
        with open('test.txt', 'r+') as file:
            lines = file.readlines()
            if "tolong" in lines[-1]:
                asyncio.run(send_message("Emergency! Fire at A20", chat_id=chat))
                
            elif "keluar" in lines[-1]:
                break

            else:
                print("no activity")
    



if __name__ == '__main__':
    asyncio.run(main())