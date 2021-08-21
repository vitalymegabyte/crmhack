from pymorphy2 import utils
from utils import lemmatize_text

class Deal():
    def __init__(self, name):
        name = utils.lemmatize_text(name)
        return(name)
