import os
import json
import codecs


class FileHelper(object):
    def write(self, path, content, append=False):
        with codecs.open(path, 'w' if not append else 'a', encoding='utf8') as f:
            f.write(content)

    def read(self, path):
        if not os.path.exists(path):
            return None
        if not os.path.isfile(path):
            return None
        with codecs.open(path, 'r') as f:
            return f.read()

    def poke_dir(self, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def get_dir_from_path(self, path):
        return os.path.dirname(path)

    def get_json(self, path):
        content =self.read(path)
        try:
            return json.loads(content)
        except:
            return None

    def write_json(self, path, content):
        self.write(path, json.dumps(content, indent=4))
