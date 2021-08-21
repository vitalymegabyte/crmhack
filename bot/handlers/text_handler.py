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
confidence = 0

def _ping_backend(update, context):
    r = requests.get('http://backend/')
    return r.text

def _create_deal(update, context):
    user = update.message.from_user
    text = update.message.text
    data = get_clients(user['id'], text)
    if len(data) == 0:
        return 'Error: no client defined'
    client = data[0]
    sum = re.search(r' (\d+) ', text)
    if not sum:
        sum = re.search(r' (\d+)$', text)
    if sum != None:
        sum = int(sum.group(0))
    deal = {'name': 'Сделка с ' + client['name'], 'company': client, 'sum': sum}
    request = requests.post('http://backend/deal/0', json=deal)
    request = requests.post('http://backend/sessions/0', json={'classname': 'Deal'})
    fast_action = {'queries': [{'url': 'http://backend/deal/0', 'method': 'post', 'json': deal}], 'text': 'Сделка зарегистрирована!'}
    fast = requests.post('http://backend/fast/0', json=fast_action)
    return 'Данные сделки:\n' + request.json()['str'] + '\nЗарегистрировать сделку: /fast' + fast.content.decode('utf-8')

actions = ['Создай сделку']
actions_tokenized = []
action_answers = {'Создай сделку': _create_deal}


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

actions_tokenized = list(map(get_vector, actions))

def text(update, context):
    request = requests.get('http://backend/user_sessions/' + str(update.message.from_user.id))
    active_sessions = request.content.decode('utf-8')
    if active_sessions == 'Active':
        pass
    else:
        index, distance = get_action(update.message.text)
        if distance >= 0.01 * (100 - confidence):
            context.bot.send_message(chat_id=update.effective_chat.id, text='Действие не определено')
        else:
            text = action_answers[actions[index]](update, context)
            context.bot.send_message(chat_id=update.effective_chat.id, text=text + '\ndistance:' + str(distance), parse_mode='HTML')

text_handler = MessageHandler(Filters.text & (~Filters.command), text)