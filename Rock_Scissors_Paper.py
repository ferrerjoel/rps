from cgitb import text
import random
from telegram import *
from telegram.ext import *
import random
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
	context.bot.send_message(update.message.chat_id, "Bienvenido. Let's Play", parse_mode=ParseMode.HTML)

	# Podemos llamar a otros comandos, sin que se haya activado en el chat (/help).
	# rick(update, context)

def dice(update, context):

	context.bot.send_message(update.message.chat_id, random.randint(1,6), parse_mode=ParseMode.HTML)
	
	

def rock(update, context):
	''' START '''
	# Enviar un mensaje a un ID determinado.
	context.bot.send_message(update.message.chat_id, "You've choose Rocks", parse_mode=ParseMode.HTML)

def scissor(update, context):
	''' START '''
	# Enviar un mensaje a un ID determinado.
	context.bot.send_message(update.message.chat_id, "You've choose Scissors", parse_mode=ParseMode.HTML)

def paper(update, context):
	''' START '''
	# Enviar un mensaje a un ID determinado.
	context.bot.send_message(update.message.chat_id, "You've choose Paper", parse_mode=ParseMode.HTML)

def game(jugada):
    
    if ((jugador > 2) or (jugador < 0)):
     print("Remember introduce: \"0\", \"1\", o \"2\".")
    elif ((jugador == (cpu+1)) or (jugador == (cpu-2))):
          resultat = "You win."
    elif ((jugador == (cpu-1)) or (jugador == (cpu+2))):
        resultat = "You lost."
    else:
        resultat = "It's a draw."

        
def main():
	TOKEN="5773831066:AAE9jjSHfF78zEa_FFjSgpP3vG5gmeMfLfU"
	updater=Updater(TOKEN, use_context=True)
	dp=updater.dispatcher

	# Eventos que activarán nuestro bot.
	# /comandos
	dp.add_handler(CommandHandler('start',	start))
	dp.add_handler(CommandHandler('dice',	dice))
	dp.add_handler(CommandHandler('game',	game))
	dp.add_handler(CommandHandler('rock',	rock))
	dp.add_handler(CommandHandler('scissor', scissor))
	dp.add_handler(CommandHandler('paper',	paper))
	

	dp.add_error_handler(error_callback)
    # Comienza el bot
	updater.start_polling()
    # Lo deja a la escucha. Evita que se detenga.
	updater.idle()

if __name__ == '__main__':
	print(('[Nombre del bot] Start...'))
	main()

KeyboardButton 
