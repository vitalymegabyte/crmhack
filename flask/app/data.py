import re
from pymorphy2 import utils
from utils import lemmatize_text
from datetime import date

class Deal():
    def create_from_session(session):
        deal = Deal(None, None, None)
        for key in session.data.keys():
            setattr(deal, key, session.data[key])
        if deal.name is None:
            if deal.date is None and deal.company is None:
                deal.name = 'Без названия от ' + date.strftime("%d %B %Y %I:%M")
            elif deal.date is None:
                deal.name =  deal.company + ' от ' + date.strftime("%d %B %Y %I:%M")
            else:
                deal.name = deal.company + ' к ' + deal.date

        return deal

    def __init__(self, id, name, company, deal_id=None, stonksNDS=None, stonks=None, status=False, responcible=None, war=True, currency=None, type=None, date=None, probability=None, orderer=None, CK=None, marja=None, NDS=True):
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
        ret = "Сделка: <b>\"" + self.name + "\"</b>\n"
        if self.status == True:
            ret = ret + "Статус: ✅закрыта \n\n"
        else:
            ret = ret + "Статус: ⏰открыта \n\n"
        if self.company is not None: ret = ret + "Компания: <b>\"" + str(self.company) + "\"</b>\n"
        else: ret = ret + "не установлена\n"
        if self.type is not None: ret = ret + str(self.type)
        if self.orderer is not None: ret = ret + "Конечный заказчик: " + str(self.orderer) + "\"\n"
        if self.stonksNDS is not None: ret = ret + "Ожидаемая прибыль с НДС: <b>" + str(self.stonksNDS)
        if self.currency is not None: ret = ret + " " + str(self.currency) + "</b>\n"
        else: "</b>\n"
        if self.stonks is not None: ret = ret + "Ожидаемая прибыль без НДС: <i>" + str(self.stonks)
        if self.currency is not None: ret = ret + " " + str(self.currency) + "</i>\n"
        else: ret = ret + "</i>\n"
        if self.probability is not None: ret = ret + "Вероятность продавца: <i>" + str(self.probability) + "</i>\n"
        if self.marja is not None: ret = ret + "Оценочная маржинальность: <i>" + str(self.marja) + "</i>\n"
        if self.date is not None: ret = ret + "Вероятная дата заключения: <b>" + str(self.date) + "</b>\n\n"
        if self.responcible is not None: ret = ret + "Ответственное лицо: <b>" + str(self.responcible) + "</b>"
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
    keywords = {"Имя": 'name','Ожидаемая выручка': 'stonks', 'Отвественное лицо': 'responcible', 'Валюта': 'currency', 'Тип сделки': 'type', 'Компания': 'company', 'Дата заключения': 'date', 'Конечный заказчик': 'orderer', 'Оценочная маржинальность': 'marja'}
    currencies = {"доллар": "USD", "бакс": "USD", "dollar": "USD", "dolar": "USD", "USD": "USD", "зелень": "USD", "вечно-зеленый": "USD", "бачинский": "USD", "долар": "USD", "евро": "EUR", "еврос": "EUR","евровалюта": "EUR", "EUR": "EUR", "евробакс": "EUR", "рубль": "RUB", "RUB": "RUB", "деревяный": "RUB", "деревянный": "RUB"}
    last_session_id = 1
    sessions = {}
    user_sessions = {}


class Session():
    classes = {'Deal': Deal}
    def __init__(self, className, id):
        self.className = className
        self.data = {}
        self.id = id
    
    def not_used_data(self):
        not_used = Data.keywords.keys()
        for key in self.data.keys():
            if key in not_used.keys():
                del not_used[key]
        return list(not_used)
    
    def __str__(self):
        str_maker = Session.classes[self.className]
        return str(str_maker)
    



Data.clients[Data.last_client_ID] = Client(Data.last_client_ID, 'ООО Ромашка')
Data.last_client_ID += 1
Data.clients[Data.last_client_ID] = Client(Data.last_client_ID, 'Кот Inc')
Data.last_client_ID += 1