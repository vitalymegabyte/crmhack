from operator import methodcaller
from os import name
from flask import request, jsonify
from app import app
from app import data
from utils import getObjectsFromText
from data import Client, Contact, Data, Deal

@app.route('/')
def home():
    return '<h1>Hello World!!!</h1>'

@app.route('/get_clients/<client_id>', methods=['GET', 'POST'])
def get_clients(client_id):
    data = request.json
    text = data['text']
    clients_got = getObjectsFromText(text, Data.clients.values())
    clients_got = list(filter(lambda c: c.normalized_name, clients_got))
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
        id = Data.last_client_ID =+ 1
        Data.clients[id] = Client(id, name)
        
@app.route('/deal/<deal_id>', methods=['GET', 'POST'])
def deal(deal_id):
    if request.method == 'GET':
        deal = Data.deals.get(deal_id)
        if deal is None:
            return 404, ""
        else:
            return jsonify(deal)
    else:
        data = request.json
        id = Data.last_deal_ID =+ 1
        name = data['name']
        deal_id = data['deal_id']
        company = data['company']
        Data.deals[id] = Deal.ID
        Data.deals[name] = Deal.name
        Data.deals[company] = Deal.company
        
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
        id = Data.last_contact_ID =+ 1
        name = data['name']
        Data.contacts[id] = Contact.ID
        Data.contacts[name] = Contact.name
