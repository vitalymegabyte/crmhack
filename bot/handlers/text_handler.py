from telegram.ext import MessageHandler, Filters
from transformers import BertModel, BertTokenizer
import torch
import scipy.spatial.distance as ds
import numpy as np

sbert = BertModel.from_pretrained('sberbank-ai/ruBert-base', output_attentions=False, output_hidden_states=False)
sbert.eval()
sbert_tokenizer = BertTokenizer.from_pretrained('sberbank-ai/ruBert-base')

actions = ['Первое действие', 'Взять', 'Запушить']
actions_tokenized = []
action_answers = {'Первое действие': 'Действую', 'Взять': 'Беру', 'Запушить': 'Я тебе что, гитхаб?!'}

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
    print(text, vector.shape)
    return vector

def get_action(text):
    vector = get_vector(text)
    distances = [ds.cosine(action_embeddings, vector) for action_embeddings in actions_tokenized]
    index = np.argmin(distances)
    return f'Текст: "{text}"\n\nПо смыслу наиболее близок к {actions[index]}\n\nПолный список распознаваемых сообщений: {actions}'

actions_tokenized = list(map(get_vector, actions))

def text(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_action(update.message.text))

text_handler = MessageHandler(Filters.text & (~Filters.command), text)