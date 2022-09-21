# -*- coding: utf-8 -*-
'''
Bot para telegram
'''
from cgitb import text
import random
from turtle import update
from telegram import *
from telegram.ext import *
from telegram import InlineKeyboardMarkup, InlineKeyboardButton # Necesario para botones

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

	Button1 = InlineKeyboardButton (
    	text = 'CARAVANA',
		url='https://www.youtube.com/watch?v=Q4sMnvX0D84'
	)
	Button2 = InlineKeyboardButton (
		text = 'Top Mundial',
		url='https://www.youtube.com/watch?v=Q4sMnvX0D84'
	)
	Button3 = InlineKeyboardButton (
		text = 'Hits del momento',
		url='https://www.youtube.com/watch?v=Q4sMnvX0D84'
	)

	update.message.reply_text (
		text = 'Elije la lista....',
		reply_markup=InlineKeyboardMarkup([
		[Button1, Button2, Button3]

		])
	)

	
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




