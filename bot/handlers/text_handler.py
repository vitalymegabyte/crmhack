from telegram.ext import MessageHandler, Filters
from transformers import BertModel, BertTokenizer
import torch

sbert = BertModel.from_pretrained('sberbank-ai/sbert_large_nlu_ru').type(torch.bfloat16)
sbert_tokenizer = BertTokenizer.from_pretrained('sberbank-ai/sbert_large_nlu_ru')

def text(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

text_handler = MessageHandler(Filters.text & (~Filters.command), text)