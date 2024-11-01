import requests
from bs4 import BeautifulSoup

from image_saver import ImageSaver

class CaptchaManager:
    def __init__(self, session, img_saver, base_url):
        self._session = session
        self._img_saver = img_saver.save
        self._base_url = base_url

    def is_captcha_page(self, html):
        return 'Вы робот?' in html
            
    def pass_captcha(self, html, url):
        while self.is_captcha_page(html):
            soup = BeautifulSoup(html, "html.parser")
            img = soup.find('img')

            self._img_saver(f'{self._base_url}{img["src"]}', 'captcha.jpg')

            enter_cap = input('Enter captcha: ') # Replace to TG

            self._res = self._send_request(enter_cap, url)
            html = self._res.text

        return self._res

    def _send_request(self, captcha, url):
        params = {'llllllll': captcha, 'submit': captcha, 
                'captcha_url': url, 
                'action_capcha_ban': '      Я не робот!     '}

        res = self._session.post(f'{self.base_url}{url}?submit={captcha}', data = params)
        return res

            

if __name__ == '__main__':
    session = requests.Session()
    img_s = ImageSaver(session, 'img/')
    base_link = 'https://otzovik.com'
    html = ''
    with open('../index.html', 'r') as f:
        html = f.read()
    

    cap = CaptchaManager(session, img_s, base_link)
    print(cap.is_captcha_page(html))
    cap.pass_captcha(html,  '/review/...')