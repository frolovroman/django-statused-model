import re


class Statuses(object):
    choices = []
    list = []
    dict = {}

    def __init__(self, choices):
        self.dict = dict(choices)
        self.list = [value for value, name in choices]
        self.choices = choices

        for value in self.list:
            label = re.sub('[^0-9a-zA-Z]+', '_', value)
            if not hasattr(self, label):
                setattr(self, label, value)

    def __call__(self, *args, **kwargs):
        return self.list

    def __getitem__(self, item):
        return self.list.__getitem__(item)

    def __iter__(self):
        return self.list.__iter__()

    def get_label(self, values):
        return self.dict.get(values)
