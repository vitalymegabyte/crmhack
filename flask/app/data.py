from pymorphy2 import utils
from utils import lemmatize_text

class Deal():
    def __init__(self, name):
        self.name = name
        self.normalized_name = lemmatize_text(name)
        self.dealID
        self.stonks_with_NDS
        self.stonks_without_NDS
        self.status
        self.responcible
        self.war
        self.currency
        #валюта
        self.type
        self.company
        self.date
        self.probability
        self.last_orderer
        self.CK
        #ЦК Сделки
        self.marja
        

class Client():
    def __init__(self, name):
        self.name = name
        self.normalized_name = lemmatize_text(name)

class Contact():
    def __init__(self, name, phone_number, email):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.normalized_name = lemmatize_text(name)