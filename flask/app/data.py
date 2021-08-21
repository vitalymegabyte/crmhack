from pymorphy2 import utils
from utils import lemmatize_text

class Deal():
    def __init__(self, id, name, deal_id, company, stonksNDS=None, stonks=None, status=True, responcible=None, war=True, currency=None, type=None, date=None, probability=None, orderer=None, CK=None, marja=None, NDS=True):
        self.id = id
        self.name = name
        self.normalized_name = lemmatize_text(name)
        self.deal_id = deal_id
        self.stonksNDS = stonksNDS
        self.stonks = stonks
        self.status = status
        self.responcible = responcible
        self.war = war
        self.currency = currency #валюта
        self.type = type
        self.company = company
        self.date = date
        self.probability = probability #вероятность продавца
        self.orderer = orderer #конечный заказчик
        self.CK = CK #ЦК Сделки
        self.marja = marja
        self.NDS = NDS

    def __dict__(self):
        return {'name': self.name, 'id': self.id, 'deal_id': self.deal_id, 'company': self.company}


class Client():
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.normalized_name = lemmatize_text(name)
    
    def __dict__(self):
        return {'id': self.id, 'name': self.name}

class Contact():
    def __init__(self, id, name, phone_number=None, email=None):
        self.id = id
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.normalized_name = lemmatize_text(name)
    def __dict__(self):
        return {'name': self.name}

    def __dict__(self):
        return {'id': self.id, 'name': self.name}

class Data():
    clients = {}
    deals = {}
    contacts = {}
    last_contact_ID = 0
    last_deal_ID = 0
    last_client_ID = 0

Data.clients[Data.last_client_ID] = Client(Data.last_client_ID, 'T1 Консалтинг')
Data.last_client_ID += 1