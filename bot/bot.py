from telegram.ext import Updater
import os
import logging
from handlers.command_handlers import start_handler
from handlers.fast_command_handler import fast_command_handler
from handlers.text_handler import text_handler

updater = Updater(token=os.environ.get('TOKEN'))
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(text_handler)
dispatcher.add_handler(fast_command_handler)

updater.start_polling()
