class Statuses(object):
    choices = []
    list = []
    dict = {}

    def __init__(self, choices):
        self.dict = dict(choices)
        self.list = [value for value, label in choices]
        self.choices = choices

        for el in self.list:
            if not hasattr(self, str(el)):
                setattr(self, str(el), el)

    def __call__(self, *args, **kwargs):
        return self.list

    def __getitem__(self, item):
        return self.list.__getitem__(item)

    def __iter__(self):
        return self.list.__iter__()

    def get_label(self, values):
        return self.dict.get(values)
