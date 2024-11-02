import requests
from bs4 import BeautifulSoup
from time import sleep
import asyncio
import json

from captcha_manager import CaptchaManager
from config_manager import ConfigManager
from session_manager import SessionManager
from image_saver import ImageSaver

class OtzovikParser:
    def __init__(self, session, base_link, links, save_review, save_index, 
                    captcha, start_index = 0, delay = 5):
        self._session = session
        self._base_link = base_link
        self._links = links
        self._start_index = start_index
        self._delay = 5

        self._pass_captcha = captcha
        self._save_review = save_review
        self._save_index = save_index

    async def start(self):
        i = self._start_index

        # print('Start', i, self._links)
        while i < len(self._links):
            # print('Get page', f'{self._base_link}{self._links[i]}')
            reviews = await self._get_one_page(f'{self._base_link}{self._links[i]}')
            # print('Success', len(reviews))
            save_review(reviews, i)
            i+=1
            self._save_index(i)

    async def _get_one_page(self, url):
        organization_page = await self._get_page(url)
        review_links = self._get_links(organization_page)
        reviews = []
        # print('review_links', len(review_links), review_links)

        for i in review_links:
            sleep(self._delay)
            review = await self._get_page(f'{self._base_link}{i}')
            info = self._get_info(review)
            reviews.append(info)
        return reviews

    async def _get_page(self, url):
        res = self._session.session.get(url)
        # print('On captha check')
        res = await self._pass_captcha(res, url)
        # print('Good html')
        bs = BeautifulSoup(res.text, 'html.parser')
        return bs

    def _get_links(self, bs):
        links = bs.find_all('a', attrs={'class': 'review-title'})
        return [i['href'] for i in links]

    def _get_info(self, bs):
        obj = {}

        # print('Save i.html')
        with open('i.html', 'w') as f:
            f.write(bs.prettify())

        worth = bs.find_all('div', attrs={'class': 'review-plus'})
        flaws = bs.find_all('div', attrs={'class': 'review-minus'})
        text = bs.find_all('div', attrs={'class': 'review-body description'})
        score = bs.find_all('div', attrs={'class': 'rating-score tooltip-right'})

        signs = {'plus': worth, 'minus': flaws, 'text': text, 'score': score}

        for key, value in signs.items():
            if len(value) > 0:
                obj[key] = value[0].text

        return obj

def save_review(reviews, index):
    with open(f'reviews/{index}.json', 'a') as f:
        f.write(json.dumps(reviews))


async def main():
    base_link = 'https://otzovik.com'
    # links = ['/reviews/sosh_93_russia_perm/', '/scripts/captcha/index.php?rand=2826178', '/reviews/sosh_93_russia_perm/', '/reviews/eco_ooooo/'] # '/scripts/captcha/index.php?rand=2822125'
    with open('../otzovik.com_urls.txt', 'r') as f:
        links = f.read().split('\n')

    session = SessionManager()
    config = ConfigManager(session)
    
    start_index = 0
    try:
        conf = config.load()
        session.loads(conf['session'])
        start_index = conf['index']
    except:
        print('Не удалось загрузить сессию')
        session.create()
        config.save_session(session.dumps())
    
    img_s = ImageSaver(session.session, 'img/')
    cap = CaptchaManager(session.session, img_s, base_link)

    p = OtzovikParser(session, base_link, links, save_review, config.save_index, 
        cap.pass_captcha, start_index=start_index)
    await p.start()

if __name__ == '__main__':
    asyncio.run(main())

    # o = OtzovikParser(None, None, None, None, None, None)
    # with open('i.html', 'r') as f:
    #     bs = BeautifulSoup(f.read(), 'html.parser')
    #     print(o._get_info(bs))


# ToDo: add log sys + add tg notification

