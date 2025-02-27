import asyncio
import os
import time
import random

from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton

load_dotenv(dotenv_path="AutoControlerMusicPost/Vars.env")

api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
source_chat = int(os.getenv('source_chat')) # Source chat @username or id
notify_id = int(os.getenv('notify_id'))
Controler_bot = os.getenv('bot_id')

PubTime = [ "10:00", "13:00", "17:00", "20:00", "23:00" ]


class Post():
    def __init__(self, post_id, url_id, song_id):
        self.post_id = post_id
        self.url_id = url_id
        self.song_id = song_id



async def main():
    app = Client("my_account", api_id, api_hash)


    await app.start()

    list = []
    chat_history = app.get_chat_history(source_chat)

    async for message in chat_history:
        list.append(message)

    messages = list[::-1]
    messages.pop(0)
    pos = 0

    Posts = []

    if len(messages) % 3 == 0 and len(messages) > 0:

        while pos + 3 < len(list):
            Posts.append(Post(post_id=messages[pos].id, url_id=messages[pos + 1].id, song_id=messages[pos + 2].id))
            pos += 3

        if len(Posts) >= 5:
            PostsToPost = random.sample(Posts, 5)

            Date = input('Введите дату (DD.MM): ')

            await app.send_message(Controler_bot, text='/start')
            await asyncio.sleep(1)

            async def press_button(app: Client, x, y):
                async for m in app.get_chat_history(Controler_bot, 1):
                    try: await asyncio.wait_for(m.click(x, y), timeout=1)
                    except: pass


            for i in range(5):
                await press_button(app, 0, 0)
                await press_button(app, 0, 0)

                await app.forward_messages(Controler_bot, source_chat, message_ids=[PostsToPost[i].post_id])
                await asyncio.sleep(1)
                await press_button(app, 0, 3)
                await asyncio.sleep(1)
                await app.forward_messages(Controler_bot, source_chat, message_ids=[PostsToPost[i].url_id])
                await asyncio.sleep(1)
                await app.forward_messages(Controler_bot, source_chat, message_ids=[PostsToPost[i].song_id])
                await app.send_message(Controler_bot, 'Далее')
                await asyncio.sleep(1)
                await press_button(app, 1, 1)
                await app.send_message(Controler_bot, f'{PubTime[i]} ' + Date)
                await asyncio.sleep(1)


            for Posts in PostsToPost:
                await app.delete_messages(source_chat, [Posts.post_id, Posts.url_id, Posts.song_id])
                await asyncio.sleep(1)



    await app.stop()

asyncio.run(main())
