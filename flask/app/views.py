from operator import methodcaller
from os import name
from flask import request, jsonify
from app import app
from app import data
from utils import getObjectsFromText
from data import Client, Contact, Data, Deal, Session

@app.route('/')
def home():
    return '<h1>Hello World!!!</h1>'

@app.route('/get_clients/<client_id>', methods=['GET', 'POST'])
def get_clients(client_id):
    data = request.json
    text = data['text']
    clients_got = getObjectsFromText(text, Data.clients.values())
    clients_got = list(map(lambda obj: obj.get_dict(), clients_got))
    return jsonify(clients_got)

@app.route('/client/<client_id>', methods=['GET', 'POST'])
def client(client_id):
    if request.method == 'GET':
        client = Data.clients.get(client_id)
        if client is None:
            return 404, ""
        else:
            return jsonify(client)
    else:
        data = request.json
        name = data['name']
        Data.last_client_ID += 1
        id = Data.last_client_ID
        Data.clients[id] = Client(id, name)
        
@app.route('/deal/<deal_id>', methods=['GET', 'POST'])
def deal(deal_id):
    if request.method == 'GET':
        deal = Data.deals.get(deal_id)
        if deal is None:
            return 404, ""
        else:
            return jsonify(deal.get_dict())
    else:
        data = request.json
        Data.last_deal_ID += 1
        id = Data.last_deal_ID
        name = data['name']
        company = data['company']
        stonks = data.get('sum')
        if not (stonks is None):
            stonks = int(stonks)
        Data.deals[id] = Deal(id, name, company['str'], stonks=stonks)
        return jsonify(Data.deals[id].get_dict())
        
@app.route('/contact/<contact_id>', methods=['GET', 'POST'])
def contact(contact_id):
    if request.method == 'GET':
        contact = Data.contacts.get(contact_id)
        if contact is None:
            return 404, ""
        else:
            return jsonify(contact)
    else:
        data = request.json
        Data.last_contact_ID += 1
        id = Data.last_contact_ID
        name = data['name']
        Data.contacts[Data.last_contact_ID] = Contact(id, name)

@app.route('/fast/<id>', methods=['GET', 'POST'])
def fast(id):
    id = int(id)
    if request.method == 'GET':
        print('get', id, 'commmands', Data.fast_commands, flush=True)
        client = Data.fast_commands[id]
        if client is None:
            return 404, ""
        else:
            return jsonify(client)
    else:
        Data.last_fast_commands_id += 1
        Data.fast_commands[Data.last_fast_commands_id] = request.json
        print('added last fast command', Data.last_fast_commands_id, 'commands:', Data.fast_commands, flush=True)
        return str(Data.last_fast_commands_id)

@app.route('/sessions/<id>', methods=['GET', 'POST'])
def sessions(id):
    id = int(id)
    if request.method == 'GET':
        client = Data.user_sessions.get(id)
        if client is None:
            return "",  404
        else:
            arr = client.not_used_data()
            print(id, arr, flush=True)
            return jsonify(arr)
    else:
        if id in Data.user_sessions:
            if request.json['name'] == 'closed':
                session = Data.user_sessions.pop(request.json['telegram_id'])
                Data.last_deal_ID += 1
                Data.deals[Data.last_deal_ID] = Deal.create_from_session(session)
                print('???????????? ??????????????????. ?????????? ???????????? ????????????:', Data.deals)

                return jsonify({'str': str(session)})
            else:
                property = request.json
                property_name = Data.keywords[property['name']]
                Data.user_sessions[id].data[property_name] = property['value']
                print('id', id, 'json', str(Data.user_sessions[id]), 'data', Data.user_sessions[id].data)
                return jsonify({'str': str(Data.user_sessions[id])})
        else:
            Data.user_sessions[request.json['telegram_id']] = Session(request.json['classname'], id, request.json['fast_action'])
            return jsonify({'str': str(Data.user_sessions[request.json['telegram_id']])})

@app.route('/user_sessions/<id>', methods=['GET'])
def user_sessions(id):
    id = int(id)
    if id in Data.user_sessions: 
        return 'Active'
    else:
        return 'Inactive'

@app.route('/active_deals', methods=['GET'])
def active_deals():
    arr = [str(deal) for deal in Data.deals.values()]
    return jsonify(arr)