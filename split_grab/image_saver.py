import requests
import shutil

class ImageSaver:
    def __init__(self, session, path):
        self._session = session
        self._path = path

    def save(self, url, file_name):
        res_img = self._session.get(url, stream=True)

        print(res_img.status_code)
        if res_img.status_code == 200:
            # with open(f'{self._path}{file_name}', 'wb') as f:
            #     res_img.raw.decode_content = True
            #     shutil.copyfileobj(res_img.raw, f) 
            return res_img

if __name__ == '__main__':
    test_link = 'https://img.freepik.com/free-photo/3d-rendering-holographic-cube_23-2150979696.jpg'

    session = requests.Session()
    s = ImageSaver(session, 'img/')
    s.save(test_link, 'test.jpg')




