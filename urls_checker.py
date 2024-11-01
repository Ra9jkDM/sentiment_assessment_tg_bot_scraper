import numpy as np

with open('otzovik.com_urls.txt', 'r') as f:
    urls = f.read().split('\n')
    print(len(urls), len(np.unique(urls)))