import logging
import os
from aiogram import Dispatcher, Bot, executor, types
import random
import re
from about import SwearingGenerator

logging.basicConfig(level=logging.INFO)

API_TOKEN = "1062275243:AAHCgytoobgT6o4mIxYuPr9jBjvbZs1U-4Y"

bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)

def auth(func):
    async def wrapper(message):
        if message["from"]["id"] == 3509295171:
            return await message.reply("Access denied", reply=False)
        return await func(message)

    return wrapper

def checkOnName(func):
    async def wrapper(message):
        name = re.sub(r'/about|/test', '', message.text).strip()
        if not name:
            return await message.reply("Введите имя!!!", reply=False)
        return await func(message)

    return wrapper


# Welcome message
@dp.message_handler(commands=["start", "help"])
@auth
async def send_welcome(message: types.Message):
    print(message)
    await message.reply(''' 
                <b>Pidor Bot</b>
This bot will tell you who you really are.
To do this, \njust type the command: /huy

/huy - расскажет кто ты есть на самом деле.

/about - расскажет о человеке по его имени. 
<i>Например:</i> <code>/about Алексей</code>

/test - тест бота.
<i>Например:</i> <code>/test Valeria</code>

Author: @likeishutin
Invite link:  <a href="https://t.me/pidrilniybot/start=huy">https://t.me/pidrilniybot</a>
''', parse_mode='html' , reply=False, disable_web_page_preview=True)


@dp.message_handler(commands=["huy"])
async def send__huy(message: types.Message):
    sentence = SwearingGenerator(message["from"]["first_name"]).getFraseConstructor()
    await message.reply(sentence, reply=False)


@dp.message_handler(commands=["about"])
@checkOnName
async def send__about__message(message: types.Message):
    name = re.sub(r'/about', '', message.text).strip()
    sentence = SwearingGenerator(name).getFraseConstructor()
    await message.reply(sentence, reply=False)


@dp.message_handler(commands=["test"])
@checkOnName
async def send__test__message(message: types.Message):
    name = re.sub(r'/test', '', message.text).strip()
    user = SwearingGenerator(name)
    sentence = "Name: {0}\nGender: {1}\nSentance: {2}".format(name, user.gender, user.getFraseConstructor())
    await message.reply(sentence, reply=False)
            


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
