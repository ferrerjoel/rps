# -*- coding: utf-8 -*-
'''
Bot para telegram
'''
from datetime import datetime
import json
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

	context.bot.send_message(update.message.chat_id,update.message.from_user.id)

	writeUserData(update.message.from_user.id, update.message.from_user.username, update.message.from_user.first_name, update.message.from_user.last_name)

	Button1 = KeyboardButton (
    	text = '/startFriendly'
	)
	Button2 = KeyboardButton (
		text = '/startCompetitive'
	)
	Button3 = KeyboardButton (
		text = '/changeMessage'
	)
	Button4 = KeyboardButton (
		text = '/seePoints'
	)

	update.message.reply_text (
		text = 'Welcome! What do you want to do?',
		reply_markup=ReplyKeyboardMarkup([
		[Button1, Button2], [Button3, Button4]

		])
	)

def writeUserData (userID, userName, firstName, lastName):
	newUserID = {"userID" : userID, "userName" : userName, "firstName" : firstName, "lastName" : lastName, "dateCreation" : str(datetime.now())}
	with open("users.json", "r+") as data:
		fileData = json.load(data)

		if not any(userDetails['userID']==userID for userDetails in fileData['userDetails']):
			fileData["userDetails"].append(newUserID)
			data.seek(0)
			json.dump(fileData, data, indent=4)

def getRandomUserID (currentUserID):
	with open("users.json", "r+") as data:
		fileData = json.load(data)
		userDetails = fileData['userDetails']
		opponentID = random.choice(userDetails)
		return opponentID['userID']

def startFriendly(update, context):
	userID = update.message.from_user.id
	with open("games.json", "r+") as data:
		fileData = json.load(data)
		opponentID = getRandomUserID(userID)
		if not any(userDetails['userID']== opponentID for userDetails in fileData['currentGames']):
			print("Searching an opponent...")
			context.bot.send_message(opponentID,"You are the chosen one")

			'''fileData["currentGames"].append(newUserID)
			data.seek(0)
			json.dump(fileData, data, indent=4)'''
		else:
			print("Game already exists")

def dice(update, context):
	context.bot.send_message(update.message.chat_id, random.randint(1,6), parse_mode=ParseMode.HTML)

def main():
	TOKEN="5740883903:AAH369a_yh2OyYg11aTcbnW4AcffOmUW9D0"
	updater=Updater(TOKEN, use_context=True)
	dp=updater.dispatcher

	# Eventos que activarán nuestro bot.
	# /comandos
	dp.add_handler(CommandHandler('start',	start))
	dp.add_handler(CommandHandler('startFriendly',	startFriendly))

	dp.add_error_handler(error_callback)
    # Comienza el bot
	updater.start_polling()
    # Lo deja a la escucha. Evita que se detenga.
	updater.idle()

if __name__ == '__main__':
	print(('[Nombre del bot] Start...'))
	main()




