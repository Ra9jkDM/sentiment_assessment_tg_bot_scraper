import json

from session_manager import SessionManager

class ConfigManager:
    main_file = 'conf.json'
    index_file = 'index.conf'

    def __init__(self, session_manager):
        self._session_manager = session_manager

    def load(self):
        config = {}
        with open(self.main_file, 'r') as f:
            config = json.loads(f.read())

        with open(self.index_file, 'r') as f:
            config['index'] = int(f.read())

        return config

    def save_session(self, session):
        session = self._session_manager.dumps()
        with open(self.main_file, 'w') as f:
            obj = json.dumps({'session': session})
            f.write(obj)

    def save_index(self, index):
        with open(self.index_file, 'w') as f:
            f.write(str(index))


if __name__ == '__main__':
    s = SessionManager()
    c = ConfigManager(s)
    c.save_index(55)
    c.save_session(s)

    print(c.load())
