# -*- coding: utf-8 -*-
'''
Bot para telegram
'''
from datetime import datetime
import json
from cgitb import text
import random
from turtle import up, update
from telegram import *
from telegram.ext import *
from telegram import InlineKeyboardMarkup, InlineKeyboardButton # Necesario para botones

# [Opcional] Recomendable poner un log con los errores que apareceran por pantalla.
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)
def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

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

ButtonRock = KeyboardButton (
	text = '/rock'
)
ButtonPaper = KeyboardButton (
	text = '/paper'
)
ButtonScissors = KeyboardButton (
	text = '/scissors'
)

def start(update, context):
	''' START '''
	# Enviar un mensaje a un ID determinado.
	context.bot.send_message(update.message.chat_id, 'Bienvenido', parse_mode=ParseMode.HTML)

	context.bot.send_message(update.message.chat_id,update.message.from_user.id)

	writeUserData(update.message.from_user.id, update.message.from_user.username, update.message.from_user.first_name, update.message.from_user.last_name)

	update.message.reply_text (
		text = 'Welcome! What do you want to do?',
		reply_markup=ReplyKeyboardMarkup([
			[Button1, Button2], [Button3, Button4]
		])
	)

def writeUserData (userID, userName, firstName, lastName):
	newUserID = {'userID' : userID, 'userName' : userName, 'firstName' : firstName, 'lastName' : lastName, 'dateCreation' : str(datetime.now()), 'inGame' : False}
	with open('users.json', 'r+') as data:
		fileData = json.load(data)

		if not any(userDetails['userID']==userID for userDetails in fileData['userDetails']):
			fileData['userDetails'].append(newUserID)
			data.seek(0)
			json.dump(fileData, data, indent=4)

def getRandomFreeUserObject (currentUserID): #Can break if there aren't any players aviable
	with open('users.json', 'r+') as data:
		fileData = json.load(data)
		userDetails = fileData['userDetails']
		userDetails = [x for x in userDetails if x['inGame'] == False]
		if len(userDetails) >= 2:
			print(userDetails)
			opponentID = currentUserID
			while opponentID == currentUserID:
				opponentID = random.choice(userDetails)['userID']
			return opponentID
		return None
		
def startFriendly(update, context):
	userID = update.message.from_user.id
	with open('games.json', 'r+') as data:
		fileData = json.load(data)
		opponentID = getRandomFreeUserObject(userID)
		if opponentID != None:
			if not any(userDetails['userID']== opponentID for userDetails in fileData['games']):
				print('Searching an opponent...')
				#Player turn: 1 = Player 1 / 2 = Player 2 / 3 = Game ended
				#Winner: 0 = game active / 1 = P1 / 2 = P2
				newGame = {'player1ID' : userID, 'player2ID' : opponentID, 'gameStarted' : str(datetime.now()), 'playerTurn' : 1, 'player1Movement' : 0, 'player2Movement' : 0,'winner' : 0 }
				#We create a game on the database
				fileData['games'].append(newGame)
				data.seek(0)
				json.dump(fileData, data, indent=4)
				with open('users.json', 'r+') as data:
					fileData = json.load(data)
					for x in fileData['userDetails']:
						if x['userID'] == userID or opponentID:
							#We set the value 'inGame' true for the 2 players
							x['inGame'] = True
				with open('users.json', 'w') as data:
					json.dump(fileData, data, indent=4)
				print(opponentID)
				startGame(userID, opponentID, context)
			else:
				print('Game already exists')
		else:
			print('No available players right now')

def startGame(userID, opponentID, context):
	with open('users.json', 'r+') as data:
		fileData = json.load(data)
		for i in fileData['userDetails']:
			if i['userID'] == userID:
				player_name = i['firstName'] + ' ' + i['lastName']
			if i['userID'] == opponentID:
				opponent_name = i['firstName'] + ' ' + i['lastName']
		context.bot.send_message(userID,'You are in a game VS ' + opponent_name)
		context.bot.send_message(opponentID,'You are in a game VS ' + player_name)
		send_movements(userID,context)
		send_movements(opponentID,context)
	
def send_movements(userID,context):
	context.bot.send_message(userID,
			text = 'What move do you want to do?',
			reply_markup=ReplyKeyboardMarkup([
			[ButtonRock, ButtonPaper, ButtonScissors],
	],one_time_keyboard=True))

def rock(context, update):
	context.bot.send_message(update.message.chat_id, 'You have choosen rock!', parse_mode=ParseMode.HTML)
def paper(context, update):
	context.bot.send_message(update.message.chat_id, 'You have choosen paper!', parse_mode=ParseMode.HTML)
def scissors(context, update):
	context.bot.send_message(update.message.chat_id, 'You have choosen scissors!', parse_mode=ParseMode.HTML)
def main():
	TOKEN='5740883903:AAH369a_yh2OyYg11aTcbnW4AcffOmUW9D0'
	updater=Updater(TOKEN, use_context=True)
	dp=updater.dispatcher

	# Eventos que activarán nuestro bot.
	# /comandos
	dp.add_handler(CommandHandler('start',	start))
	dp.add_handler(CommandHandler('startFriendly',	startFriendly))

	dp.add_handler(CommandHandler('rock',	rock))
	dp.add_handler(CommandHandler('paper',	paper))
	dp.add_handler(CommandHandler('scissors',	scissors))

	dp.add_error_handler(error_callback)
    # Comienza el bot
	updater.start_polling()
    # Lo deja a la escucha. Evita que se detenga.
	updater.idle()

if __name__ == '__main__':
	print(('[Nombre del bot] Start...'))
	main()




