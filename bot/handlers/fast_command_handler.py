import json
import requests
from requests.api import request
from telegram.ext import MessageHandler, Filters
from telegram.ext.filters import DataDict

def fast_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='all_text:' + update.message.text)
    text = update.message.text
    text = text[5:]
    url = "http://backend/fast/" + text
    r = requests.get(url)
    data = r.json()
    
    for i in data['queries']:
        getattr(requests, i['method'])(i['url'], json=i.get('json'))
    context.bot.send_message(chat_id=update.effective_chat.id, text=data['text'])

fast_command_handler = MessageHandler(Filters.text, fast_command)