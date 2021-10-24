from dataclasses import dataclass
from telegram.ext import MessageHandler, Filters
from transformers import BertModel, BertTokenizer
import torch
import scipy.spatial.distance as ds
import numpy as np
import requests
import re
from utils import get_clients

sbert = BertModel.from_pretrained('sberbank-ai/ruBert-base', output_attentions=False, output_hidden_states=False)
sbert.eval()
sbert_tokenizer = BertTokenizer.from_pretrained('sberbank-ai/ruBert-base')
confidence = 80

def _ping_backend(update, context):
    r = requests.get('http://backend/')
    return r.text

def _create_deal(update, context):
    user = update.message.from_user
    text = update.message.text
    data = get_clients(user['id'], text)
    #if len(data) == 0:
    #    return 'Error: no client defined'
    client = None if len(data) == 0 else data[0]
    sum = re.search(r' (\d+) ', text)
    if not sum:
        sum = re.search(r' (\d+)$', text)
    if sum != None:
        sum = int(sum.group(0))
    deal = {'company': client}
    if not (sum is None):
        deal['sum'] = sum
    fast_action = {'queries': [{'url': 'http://backend/sessions/' + str(user['id']), 'method': 'post', 'json': {'name': 'closed', 'telegram_id': user['id']}}], 'text': 'Сделка зарегистрирована!'}
    fast = requests.post('http://backend/fast/0', json=fast_action)
    request = requests.post('http://backend/sessions/0', json={'classname': 'Deal', 'telegram_id': user['id'], 'fast_action': fast.content.decode('utf-8')})
    if client:
        request = requests.post('http://backend/sessions/' + str(user['id']), json={'name': 'Компания', 'value': client['name']})
    if sum:
        request = requests.post('http://backend/sessions/' + str(user['id']), json={'name': 'Сумма', 'value': client['sum']})
    #request = requests.post('http://backend/deal/0', json=deal)
    return 'Данные сделки:\n' + request.json()['str']

def _current_deal(update, context):
    request = requests.get('http://backend/active_deals')
    data = request.json()
    if len(data) == 0:
        return "<b>Сделок нет</b>"
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='<b>Текущие сделки</b>', parse_mode='HTML')
        for d in data:
            context.bot.send_message(chat_id=update.effective_chat.id, text=d, parse_mode='HTML')
    return ''

actions = ['Создай сделку', 'Текущие сделки']
actions_tokenized = []
action_answers = {'Создай сделку': _create_deal, 'Текущие сделки': _current_deal}


def _sbert_tokenize_sentence(text):
    encoded_dict = sbert_tokenizer.encode_plus(
                        text,                      # Sentence to encode.
                        add_special_tokens = False, # Add '[CLS]' and '[SEP]'
                        max_length = 64,           # Pad & truncate all sentences.
                        return_tensors = 'pt',
                        padding = 'max_length',
                        truncation=True
                   )
    return encoded_dict['input_ids'].reshape([1, -1])

def _sbert_get_vector(input_ids):
    embeddings = sbert(input_ids)
    return embeddings['last_hidden_state'].reshape([1, -1]).detach().numpy()

def get_vector(text):
    input_ids = _sbert_tokenize_sentence(text)
    vector = _sbert_get_vector(input_ids)
    return vector

def get_action(text):
    vector = get_vector(text)
    distances = [ds.cosine(action_embeddings, vector) for action_embeddings in actions_tokenized]
    index = np.argmin(distances)
    return index, distances[index]

def get_nearest_word(text, words):
    text_vector = get_vector(text)
    word_vectors = [get_vector(word) for word in words]

    distances = [ds.cosine(action_embeddings, text_vector) for action_embeddings in word_vectors]
    index = np.argmin(distances)
    return index, distances[index]

actions_tokenized = list(map(get_vector, actions))

def text(update, context):
    user = update.message.from_user
    text = update.message.text
    
    request = requests.get('http://backend/user_sessions/' + str(update.message.from_user.id))
    active_sessions = request.content.decode('utf-8')
    if active_sessions == 'Active':
        request = requests.get('http://backend/sessions/' + str(update.message.from_user.id))
        data = request.json()
        var_name = get_nearest_word(update.message.text, data)
        var_name = data[var_name[0]]
        if var_name == 'Компания' or var_name == 'Сумма':# or var_name == 'Валюта':
            value = None
            if var_name == 'Компания':
                data = get_clients(user['id'], text)
                value = None if len(data) == 0 else data[0]['name']
            elif var_name == 'Сумма':
                sum = re.search(r' (\d+) ', text)
                if not sum:
                    sum = re.search(r' (\d+)$', text)
                if sum != None:
                    sum = int(sum.group(0))
                value = sum
            if value != None:
                request = requests.post('http://backend/sessions/' + str(user['id']), json={'name': var_name, 'value': value})
                context.bot.send_message(chat_id=update.effective_chat.id, text=request.json()['str'], parse_mode='HTML')
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Действие не распознано', parse_mode='HTML')
    else:
        index, distance = get_action(update.message.text)
        if distance >= 0.01 * (100 - confidence):
            context.bot.send_message(chat_id=update.effective_chat.id, text='Действие не определено')
        else:
            text = action_answers[actions[index]](update, context)
            answer = text
            context.bot.send_message(chat_id=update.effective_chat.id, text=answer, parse_mode='HTML')

text_handler = MessageHandler(Filters.text & (~Filters.command), text)