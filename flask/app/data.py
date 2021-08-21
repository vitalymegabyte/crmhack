from pymorphy2 import utils
from utils import lemmatize_text

class Client():
    def __init__(self, name):
        self.name = name
        self.normalized_name = lemmatize_text(name)

clients = dict(map(lambda x: (x.normalized_name, x), [Client('T1 Консалтинг')]))