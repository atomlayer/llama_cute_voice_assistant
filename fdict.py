import json


class fdict(dict):

    def _load_from_json(self):
        try:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                return json.load(file)
        except:
            return {}

    def __init__(self, file_name, seq=None, **kwargs):
        self.file_name = file_name
        data = self._load_from_json()
        if seq is not None:
            data.update(seq)
        data.update(kwargs)
        super(fdict, self).__init__(data)
        self.save_to_json()

    def save_to_json(self):
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(self, file, ensure_ascii=False)

    def update(self, seq=None, **kwargs):
        data = {}
        if seq is not None:
            data.update(seq)
        data.update(kwargs)
        super(fdict, self).update(data)
        self.save_to_json()

    def clear(self):
        self.clear()
        self.save_to_json()

    def pop(self, k, d=None):
        super(fdict, self).pop(k, d)
        self.save_to_json()

    def popitem(self):
        super(fdict, self).popitem()
        self.save_to_json()

    def setdefault(self, *args, **kwargs):
        super(fdict, self).setdefault(args, kwargs)
        self.save_to_json()

    def __delitem__(self, arg):
        super().__delitem__(arg)
        self.save_to_json()

    def __setitem__(self, key, value):
        self.update({key: value})
