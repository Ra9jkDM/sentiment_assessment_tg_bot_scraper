import requests
from fake_headers import Headers
import pickle
import base64

class SessionManager:
    def __init__(self, session = None):
        self._session = session

    def create(self):
        header = Headers(
            browser="chrome", 
            os="win",  
            headers=True 
        )
        new_headers = header.generate()
        self._session = requests.Session()
        self._session.headers.update(new_headers)

    def dumps(self):
        obj = pickle.dumps(self._session)
        obj = base64.b64encode(obj)
        return obj.decode('utf-8')

    def loads(self, obj):
        obj = obj.encode('utf-8')
        obj = base64.b64decode(obj)
        self._session = pickle.loads(obj)

    @property
    def session(self):
        return self._session


if __name__ == '__main__':
    s = SessionManager()
    s.create()
    print(s.session.get('https://google.com/'))
    print(s.session.cookies)
    obj = s.dumps()
    
    s = SessionManager()
    s.loads(obj)
    print(s.session.cookies)
    print(s.session.get('https://google.com/'))