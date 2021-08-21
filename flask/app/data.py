from pymorphy2 import utils
from utils import lemmatize_text

class Deal():
    def __init__(self, id, name, company, deal_id=None, stonksNDS=None, stonks=None, status=True, responcible=None, war=True, currency="у.е.", type=None, date=None, probability=None, orderer=None, CK=None, marja=None, NDS=True):
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

    def get_dict(self):
        return {'name': self.name, 'id': self.id, 'deal_id': self.deal_id, 'company': self.company, 'str': str(self)}

    def __str__(self):
        ret = self.name + "\n"
        ret = ret + 'Компания: ' + str(self.company) + "\n"
        if self.stonks is not None: ret = ret + "Сумма: " + str(self.stonks)
        return ret


class Client():
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.normalized_name = lemmatize_text(name)
    
    def get_dict(self):
        return {'id': self.id, 'name': self.name, 'str': str(self)}

    def __str__(self):
        return self.name

class Contact():
    def __init__(self, id, name, phone_number=None, email=None):
        self.id = id
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.normalized_name = lemmatize_text(name)
    def get_dict(self):
        return {'name': self.name}

    def get_dict(self):
        return {'id': self.id, 'name': self.name}

class Data():
    clients = {}
    deals = {}
    contacts = {}
    last_contact_ID = 0
    last_deal_ID = 0
    last_client_ID = 0
    fast_commands = {}
    last_fast_commands_id = 0
    keywords = {"Имя": 'name','Ожидаемая выручка': 'stonks', 'Ответственное лицо': 'responcible', 'Валюта': 'currency', 'Тип сделки': 'type', 'Компания': 'company', 'Дата заключения': 'date', 'Конечный заказчик': 'orderer', 'Оценочная маржинальность': 'marja'}


Data.clients[Data.last_client_ID] = Client(Data.last_client_ID, 'T1 Консалтинг')
Data.last_client_ID += 1