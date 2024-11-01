import json
import pickle
import base64
import os

class Parser:
    config_file = 'parser_config'
    _idx = 0
    _session = None

    def __init__(self, url_file):
        self._url_file = url_file

        if self.is_config_exists():
            self._load_progress()
        else:
            self._save_progress()

    def is_config_exists(self):
        return os.path.exists(self.config_file)

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
    # parser.start()
    obj = pickle.dumps(parser)
    print(obj)
    obj_base64 = base64.b64encode(obj)
    print(obj_base64.decode('utf-8').encode('utf-8'))


# load session and headers OR create
# try get page from list
    # if detect capcha -> send to TG
    #  [with info Example: get 100 pages - 60% -positive 40% negative
    #   60 -positive, ..., size of all grabbed files]
    # get user enter