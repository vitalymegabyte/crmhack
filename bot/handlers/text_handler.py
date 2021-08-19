from telegram.ext import MessageHandler, Filters

def text(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

text_handler = MessageHandler(Filters.text & (~Filters.command), text)