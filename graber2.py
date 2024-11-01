from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import json
chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)

isFirstTime = True
#https://chromewebstore.google.com/detail/setupvpn-lifetime-free-vp/oofgbpoabipfcfjapgnbbjjaenockbdp?hl=en-US&utm_source=ext_sidebar
main_link = 'https://otzovik.com/reviews/institut_ekonomiki_upravleniya_i_socialnih_otnosheniy_russia_moscow/'
base_link = 'https://otzovik.com'
dir_name = 'reviews'

def get_page(url):
    global isFirstTime
    # res = requests.get(url, headers={'User-Agent': user_agent})#, proxies=proxies)
    driver.get(url)
    if isFirstTime:
        input()
        isFirstTime = False

    if 'Вы робот?' in str(driver.page_source):
        print('Enter capcha')
        input()
    bs = BeautifulSoup(driver.page_source, 'html.parser')
    return bs

def get_links(bs):
    links = bs.find_all('a', attrs={'class': 'review-title'})
    return [i['href'] for i in links]

def get_review(bs):
    obj = {}

    worth = bs.find_all('div', attrs={'class': 'review-plus'})
    flaws = bs.find_all('div', attrs={'class': 'review-minus'})
    text = bs.find_all('div', attrs={'class': 'review-body description'})
    score = bs.find_all('div', attrs={'class': 'rating-score tooltip-right'})


    # print(worth, flaws, text, score)
    if len(worth) >= 1:
        obj['plus'] = worth[0].text

    if len(flaws) >= 1:
        obj['minus'] = flaws[0].text
    if len(text) >= 1:
        obj['text'] = text[0].text
    else:
        print('No text!!!')
    if len(score) >= 1:
        obj['score'] = int(score[0].text.replace('\n', ''))
    else:
        print('No score|||')
    
    return obj
    
def get_reviews(url):
    # print(url)
    bs = get_page(url)
    links = get_links(bs)
    # print(links, bs)
    reviews = []
    for i in links:
        # print(i)
        sleep(5)
        bs = get_page(base_link+i)
        reviews.append(get_review(bs))
    print('\t'+str(len(links)))
    return reviews

def save_reviews(file_name, reviews):
    with open(dir_name+'/'+file_name, 'a') as f:
        f.write(json.dumps(reviews))

def read_links(path):
    with open(path, 'r') as f:
        return f.read().split('\n')[:-1]

if __name__ == '__main__':
    # x = get_reviews(main_link)
    links = read_links('otzovik.com_urls.txt')

    i = 7853
    while i < len(links):
        print(f'[{i}] {links[i]}')
        try:
            x = get_reviews(base_link+links[i])
            x = {'review_list': x}
            save_reviews(f'{i}.txt', x)
        except:
            input()
        i+=1



    driver.close()

# https://otzovik.com/review_14254597.html?&capt4a=3401729753463268

# source ../Курсач/.venv/bin/activate
# https://chromewebstore.google.com/detail/free-vpn-zenmate-best-vpn/fdcgdnkidjaadafnichfpabhfomcebme


# https://otzovik.com/review_14658929.html
# https://otzovik.com/review_16590518.html
# https://otzovik.com/review_16097449.html
# https://otzovik.com/review_14493075.html
# https://otzovik.com/review_14800792.html