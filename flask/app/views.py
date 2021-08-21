from flask import request, jsonify
from app import app
from utils import getObjectsFromText
from data import clients

@app.route('/')
def home():
    return '<h1>Hello World!!!</h1>'

@app.route('/get_clients/<client_id>', methods=['GET', 'POST'])
def get_clients(client_id):
    data = request.json
    text = data['text']
    clients_got = getObjectsFromText(text, clients.values())
    clients_got = list(map(lambda c: c.name, clients_got))
    return jsonify(clients_got)