# -*- coding: utf-8 -*-
'''
Bot para telegram
'''
from cgitb import text
import random
from telegram import *
from telegram.ext import *
# from requests import *

# [Opcional] Recomendable poner un log con los errores que apareceran por pantalla.
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)
def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def start(update, context):
	''' START '''
	# Enviar un mensaje a un ID determinado.
	context.bot.send_message(update.message.chat_id, "Bienvenido", parse_mode=ParseMode.HTML)

	# Podemos llamar a otros comandos, sin que se haya activado en el chat (/help).
	# rick(update, context)
def rick(update, context):

	cid=update.message.chat_id
	msg="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
	# Responde directametne en el canal donde se le ha hablado.
	update.message.reply_text(msg)

def dice(update, context):

	context.bot.send_message(update.message.chat_id, random.randint(1,6), parse_mode=ParseMode.HTML)

def main():
	TOKEN="5740883903:AAH369a_yh2OyYg11aTcbnW4AcffOmUW9D0"
	updater=Updater(TOKEN, use_context=True)
	dp=updater.dispatcher

	# Eventos que activarán nuestro bot.
	# /comandos
	dp.add_handler(CommandHandler('start',	start))
	dp.add_handler(CommandHandler('rick',	rick))
	dp.add_handler(CommandHandler('dice',	dice))

	dp.add_error_handler(error_callback)
    # Comienza el bot
	updater.start_polling()
    # Lo deja a la escucha. Evita que se detenga.
	updater.idle()

if __name__ == '__main__':
	print(('[Nombre del bot] Start...'))
	main()

KeyboardButton 

