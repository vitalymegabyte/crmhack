from telegram.ext import MessageHandler, Filters

def fast_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='all_text:' + update.message.text)

fast_command_handler = MessageHandler(Filters.text, fast_command)