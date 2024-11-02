import os

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import BufferedInputFile


API_TOKEN = os.environ.get('TOKEN')
USER_ID = os.environ.get('USER_ID')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)


dp = Dispatcher()


answer = ''

# @dp.message(Command("start"))
# async def cmd_start(message: types.Message):
#     print('User id', message.from_user.id)
#     await message.answer("Hello!")

# @dp.message()
async def cmd_answer(message: types.Message):
    global answer
    print(message.text)
    answer = message.text
    await dp.stop_polling()

# async def send_message(chat_id, text):
#     await bot.send_message(chat_id, text)

async def main():
    global answer
    # print(dir(dp.message.register))

    photo = ''
    with open('../img/c1.jpg', 'rb') as f:
        photo = BufferedInputFile(f.read(), 'captcha.jpg')

    await bot.send_photo(chat_id=USER_ID, caption='Enter captcha:', photo=photo)

    # await bot.send_message(chat_id=USER_ID, text='Enter captcha:')

    dp.message.register(cmd_answer)

    await dp.start_polling(bot)
    print('x', answer)

if __name__ == "__main__":
    asyncio.run(main())

# tg_manager.py


# https://docs.aiogram.dev/en/latest/dispatcher/dispatcher.html#aiogram.dispatcher.dispatcher.Dispatcher.stop_polling
# async stop_polling() 
# https://mastergroosha.github.io/aiogram-3-guide/messages/