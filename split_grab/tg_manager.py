import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import BufferedInputFile

import requests
import shutil
from image_saver import ImageSaver

API_TOKEN = os.environ.get('TOKEN')
USER_ID = os.environ.get('USER_ID')
logging.basicConfig(level=logging.CRITICAL)

class TG_manager:
    def __init__(self):
        self._bot = Bot(token=API_TOKEN)
        self._dp = Dispatcher()
        self._dp.message.register(self._get_answer)
        self._answer = ''

    async def send_question(self, img, text):
        img = BufferedInputFile(img, 'captcha.jpg')
        await self._bot.send_photo(chat_id=USER_ID, photo=img, caption=text)

    async def get_answer(self):
        await self._dp.start_polling(self._bot)
        return self._answer

    async def _get_answer(self, message: types.Message):
        self._answer = message.text
        await self._dp.stop_polling()


async def main():
    tg = TG_manager()

    test_link = 'https://img.freepik.com/free-photo/3d-rendering-holographic-cube_23-2150979696.jpg'
    session = requests.Session()

    # with open('../img/c1.jpg', 'rb') as f:
    #     photo = f.read()

    s = ImageSaver(session, 'img/')
    photo = s.save(test_link, 'test.jpg')
    # print(photo)

    await tg.send_question(photo.content, 'Введите капчу:')
    answer = await tg.get_answer()
    print('Ответ:', answer)

if __name__ == '__main__':
    asyncio.run(main())