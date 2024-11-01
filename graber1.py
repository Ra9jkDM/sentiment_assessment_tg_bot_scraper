import requests
import json
import pickle
import base64
import os
from fake_headers import Headers
from bs4 import BeautifulSoup
import shutil
from time import sleep

class Parser:
    config_file = 'parser_config.json'
    base_url = 'https://otzovik.com'
    img_dir = 'captcha_img'
    pages_dir = 'reviews'
    _url_list = []
    _idx = 0
    _session = None

    def __init__(self, url_file):
        self._url_file = url_file

        self._try_create_working_dirs()

        if self.is_config_exists():
            try:
                self._load_progress()
            except:
                self._create_session()
                self._save_progress()
        else:
            self._create_session()
            self._save_progress()

    def is_config_exists(self):
        return os.path.exists(self.config_file)

    def start(self):
        self._load_urls()

        print(self._idx, len(self._url_list), f'{self.base_url}{self._url_list[self._idx]}')
        while self._idx < len(self._url_list):
            response = self._session.get(f'{self.base_url}{self._url_list[self._idx]}')
            status_code = response.status_code

            print(status_code)
            if status_code == 200:
                while 'Вы робот?' in response.text: # если ошибка в captha
                    response = self._pass_captcha(response.text)

                links = self._get_links(response.text)
                print('\t', len(links))
                reviews = self._get_reviews(links)
                self._save_reviews(self._idx, reviews)
                
                self._idx += 1
                print(f'{self.base_url}{self._url_list[self._idx-1]}', self._idx)
                self._save_progress()

    def _get_links(self, html):
        bs = BeautifulSoup(html, 'html.parser')
        links = bs.find_all('a', attrs={'class': 'review-title'})
        return [i['href'] for i in links]

    def _get_reviews(self, links):
        reviews = []
        for i in links:
            sleep(5)
            bs = self._get_page(self.base_url+i)
            reviews.append(self._get_review(bs))
        return reviews

    def _get_page(self, page):
        res = self._session.get(page)
        bs = BeautifulSoup(res.text, 'html.parser')
        return bs

    def _get_review(self, bs):
        obj = {}

        worth = bs.find_all('div', attrs={'class': 'review-plus'})
        flaws = bs.find_all('div', attrs={'class': 'review-minus'})
        text = bs.find_all('div', attrs={'class': 'review-body description'})
        score = bs.find_all('div', attrs={'class': 'rating-score tooltip-right'})


        if len(worth) >= 1:
            obj['plus'] = worth[0].text

        if len(flaws) >= 1:
            obj['minus'] = flaws[0].text
        if len(text) >= 1:
            obj['text'] = text[0].text
        if len(score) >= 1:
            obj['score'] = int(score[0].text.replace('\n', ''))
        
        return obj
    
    def _save_reviews(self, file_name, reviews):
        with open(f'{self.pages_dir}/{file_name}.json', 'w') as f:
            f.write(json.dumps(reviews))

    def _load_urls(self):
        with open(self._url_file, 'r') as f:
            urls = f.read()
            self._url_list = urls.split('\n')

    def _pass_captcha(self, html):
        soup = BeautifulSoup(html, "html.parser")
        img = soup.find('img')

        res_img = self._session.get(self.base_url + img['src'], stream=True)
        if res_img.status_code == 200:
            with open(self.img_dir+'captcha.jpg', 'wb') as f:
                res_img.raw.decode_content = True
                shutil.copyfileobj(res_img.raw, f) 

        enter_cap = input('Enter captcha: ') # Replace to TG

        params = {'llllllll': enter_cap, 'submit': enter_cap, 
            'captcha_url': self._url_list[self._idx], 
            'action_capcha_ban': '      Я не робот!     '}

        res = self._session.post(f'{self.base_url}{self._url_list[self._idx]}?submit={enter_cap}', data = params)
        return res

    def _create_session(self):
        header = Headers(
            browser="chrome", 
            os="win",  
            headers=True 
        )
        new_headers = header.generate()
        sess = requests.Session()
        sess.headers.update(new_headers)
        self._session = sess

    def _try_create_working_dirs(self):
        for i in [self.img_dir, self.pages_dir]:
            if not os.path.exists(i):
                os.mkdir(i)

    def _save_progress(self):
        state = {'url_file': self._url_file, 'index': self._idx}

        if self._session:
            obj = pickle.dumps(self._session)
            obj_base64 = base64.b64encode(obj)
            state['session'] = obj_base64.decode('utf-8')

        with open(self.config_file, 'w') as f:
            f.write(json.dumps(state))

    def _load_progress(self):
        with open(self.config_file, 'r') as f:
            config = f.read()
            config = json.loads(config)

            if self._url_file != config['url_file']:
                print('Файлы со ссылками отличаются.')
                answer = input('Продолжить (1), начать с нуля(2): ')
                if answer == '2':
                    config['index'] = 0
            
            self._idx = config['index']

            if 'session' in config:
                obj_base64 = config['session']
                obj = base64.b64decode(obj_base64)
                obj = obj.encode('utf-8')

                self._session = pickle.loads(obj)






if __name__ == '__main__':
    parser = Parser('otzovik.com_urls.txt')
    parser.start()
    # obj = pickle.dumps(parser)
    # print(obj)
    # obj_base64 = base64.b64encode(obj)
    # print(obj_base64.decode('utf-8').encode('utf-8'))


# load session and headers OR create
# try get page from list
    # if detect capcha -> send to TG
    #  [with info Example: get 100 pages - 60% -positive 40% negative
    #   60 -positive, ..., size of all grabbed files]
    # get user enter

# ToDo:
# - создать структуру диплома
# - протестить данный код с капчей
# - разделить на классы
# - добавить: чтобы отправлял капчу в TG и получал ответ