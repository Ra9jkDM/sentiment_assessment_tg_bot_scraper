import requests
from bs4 import BeautifulSoup
import glob

from image_saver import ImageSaver
from tg_manager import TG_manager

def work_status():
    total  = -1
    loaded = len(glob.glob('reviews/*'))

    with open('../otzovik.com_urls.txt', 'r') as f:
        total = len(f.read().split('\n'))

    return f'Загружено: {loaded} из {total}'

class CaptchaManager:
    def __init__(self, session, img_saver, base_url):
        self._session = session
        self._img_saver = img_saver.save
        self._base_url = base_url
        self._tg = TG_manager()

    def is_captcha_page(self, html):
        return 'Вы робот?' in html
            
    async def pass_captcha(self, res, url):
        # print(res.text, self.is_captcha_page(res.text))
        # input('wait')
        while self.is_captcha_page(res.text):
            print('Found captha')
            soup = BeautifulSoup(res.text, "html.parser")
            img = soup.find('img')

            img = self._img_saver(f'{self._base_url}{img["src"]}', 'captcha.jpg')
            print(img, type(img))
            # enter_cap = input('Enter captcha: ') # Replace to TG
            status = work_status()
            await self._tg.send_question(img.content, f'{status}\nВведите капчу:')
            answer = await self._tg.get_answer()

            res = self._send_request(answer, url)

        return res

    def _send_request(self, captcha, url):
        url = url[len(self._base_url):]
        params = {'llllllll': captcha, 'submit': captcha, 
                'captcha_url': url, 
                'action_capcha_ban': '      Я не робот!     '}

        # print(f'{self._base_url}{url}?submit={captcha}', self._base_url, url)
        # input('await')
        res = self._session.post(f'{self._base_url}{url}?submit={captcha}', data = params)
        return res

            

if __name__ == '__main__':
    print(work_status())
    session = requests.Session()
    img_s = ImageSaver(session, 'img/')
    base_link = 'https://otzovik.com'
    html = ''
    with open('../index.html', 'r') as f:
        html = f.read()
    

    cap = CaptchaManager(session, img_s, base_link)
    print(cap.is_captcha_page(html))
    cap.pass_captcha(html,  '/review/...')