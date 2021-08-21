from pymorphy2 import utils
from utils import lemmatize_text

class Deal():
    def __init__(self, ID, name, dealID, company, stonksNDS=None, stonks=None, status=True, responcible=None, war=True, currency=None, type=None, date=None, probability=None, orderer=None, CK=None, marja=None, NDS=True):
        self.ID = ID
        self.name = name
        self.normalized_name = lemmatize_text(name)
        self.dealID = dealID
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


class Client():
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name
        self.normalized_name = lemmatize_text(name)

class Contact():
    def __init__(self, ID, name, phone_number, email):
        self.ID = ID
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.normalized_name = lemmatize_text(name)

class Data():
    clients = {}
    deals = {}
    contacts = {}
    last_contact_ID = 0
    last_deal_ID = 0
    last_client_ID = 0
    