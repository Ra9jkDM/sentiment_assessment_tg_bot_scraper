import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import shutil
# https://docs-python.ru/packages/modul-requests-python/sessii-seansy-session/
# https://pypi.org/project/fake-headers/

header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )
h = header.generate()
base_url = 'https://otzovik.com'

print(h)
sess = requests.Session()
sess.headers.update(h)

url = 'https://otzovik.com/reviews/elektronniy_polis_osago_tinkoff_strahovanie/'
res = sess.get(url)

print('Text', res.text, '\n'*4)
print('Cookies', res.cookies, '\n'*4)

# input()
# res = sess.get(url) #, cookies=res.cookies)

# print('Text', res.text, '\n'*4)
# print('Cookies', res.cookies, '\n'*4)

def save_captcha(page, sess):
    page = ''
    with open('index.html', 'r') as f:
        page = f.read()

    soup = BeautifulSoup(page, "html.parser")
    tags=soup.find('img')

    print(base_url+tags['src'])
    r = sess.get(base_url+tags['src'], stream=True)

    if r.status_code == 200:
        with open('c1.jpg', 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f) 

save_captcha(res.text, sess)
enter_cap = input('Enter captcha:')
print(enter_cap)

params = {'llllllll': enter_cap, 'submit': enter_cap, 
    'captcha_url': '/reviews/elektronniy_polis_osago_tinkoff_strahovanie/', 'action_capcha_ban': '      Я не робот!     '}
res = sess.post(url+f'?submit={enter_cap}', data = params)

print('Text', res.text, '\n'*4)
print('Cookies', res.cookies, '\n'*4)
# Работает
# ToDo: сохранять cookies and headers

# https://otzovik.com/reviews/elektronniy_polis_osago_tinkoff_strahovanie/?submit=567ff&capt4a=