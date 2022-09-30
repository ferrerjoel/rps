# -*- coding: utf-8 -*-
'''
Bot para telegram
'''
from datetime import datetime
import json
from cgitb import text
import random
from shutil import move
from turtle import up, update
from telegram import *
from telegram.ext import *
# Necesario para botones
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

# [Opcional] Recomendable poner un log con los errores que apareceran por pantalla.
import logging

NUMBER_ROUNDS_WIN = 3

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


Button1 = KeyboardButton(
    text='/startFriendly'
)
Button2 = KeyboardButton(
    text='/startCompetitive'
)
Button3 = KeyboardButton(
    text='/changeMessage'
)
Button4 = KeyboardButton(
    text='/seePoints'
)

ButtonRock = KeyboardButton(
    text='/rock'
)
ButtonPaper = KeyboardButton(
    text='/paper'
)
ButtonScissors = KeyboardButton(
    text='/scissors'
)


def start(update, context):
    ''' START '''
    # Enviar un mensaje a un ID determinado.
    context.bot.send_message(update.message.chat_id,
                             'Welcome to RPS Project!', parse_mode=ParseMode.HTML)

    context.bot.send_message(update.message.chat_id,
                             update.message.from_user.id)

    writeUserData(update.message.from_user.id, update.message.from_user.username,
                  update.message.from_user.first_name, update.message.from_user.last_name)

    update.message.reply_text(
        text='Welcome! What do you want to do?',
        reply_markup=ReplyKeyboardMarkup([
            [Button1, Button2], [Button3, Button4]
        ])
    )

def writeUserData(userID, userName, firstName, lastName):
    newUserID = {'userID': userID, 'userName': userName, 'firstName': firstName,
                 'lastName': lastName, 'message' : "Hey there! I'm using RPS Project",'dateCreation': str(datetime.now()), 'inGame': False}
    with open('users.json', 'r+') as data:
        fileData = json.load(data)

        if not any(userDetails['userID'] == userID for userDetails in fileData['userDetails']):
            fileData['userDetails'].append(newUserID)
            data.seek(0)
            json.dump(fileData, data, indent=4)

def getRandomFreeUserObject(currentUserID):
    with open('users.json', 'r+') as data:
        fileData = json.load(data)
        userDetails = fileData['userDetails']
        userDetails = [x for x in userDetails if x['inGame'] == False]
        if len(userDetails) >= 2:
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
            if not any(userDetails['userID'] == opponentID for userDetails in fileData['games']):
                print('Searching an opponent...')
                # Player turn: 1 = Player 1 / 2 = Player 2 / 3 = Game ended
                # Winner: 0 = game active / 1 = P1 / 2 = P2
                newGame = {'player1ID': userID, 'player2ID': opponentID, 'gameStarted': str(datetime.now(
                )), 'player1Movement': 0, 'player2Movement': 0, 'player1Rounds': 0, 'player2Rounds': 0, 'isActive' : True}
                # We create a game on the database
                fileData['games'].append(newGame)
                data.seek(0)
                json.dump(fileData, data, indent=4)
                with open('users.json', 'r+') as data:
                    fileData = json.load(data)
                    for x in fileData['userDetails']:
                        if x['userID'] == userID or x['userID'] == opponentID:
                            # We set the value 'inGame' true for the 2 players
                            x['inGame'] = True
                with open('users.json', 'w') as data:
                    json.dump(fileData, data, indent=4)
                print(opponentID)
                startGame(userID, opponentID, context)
            else:
                print('Game already exists')
        else:
            print('No available players right now')
            context.bot.send_message(update.message.chat_id, "There aren't any available players right now :(", parse_mode=ParseMode.HTML)


def startGame(userID, opponentID, context):
    with open('users.json', 'r+') as data:
        fileData = json.load(data)
        for i in fileData['userDetails']:
            if i['userID'] == userID:
                # If the user doesn't have a last name we don't use it
                player_name = i['firstName'] + ' ' + (i['lastName'] if i['lastName'] is not None else '')
                player_message = i['message']
            if i['userID'] == opponentID:
                opponent_name = i['firstName'] + ' ' + (i['lastName'] if i['lastName'] is not None else '')
                opponent_message = i['message']
        context.bot.send_message(
            userID, 'You are in a game VS ' + opponent_name + '\n"'+opponent_message+'"')
        context.bot.send_message(
            opponentID, 'You are in a game VS ' + player_name + '\n"'+player_message+'"')
        send_movements(userID, context)
        send_movements(opponentID, context)


def send_movements(userID, context):
    context.bot.send_message(userID,
                             text='What move do you want to do?',
                             reply_markup=ReplyKeyboardMarkup([
                                 [ButtonRock, ButtonPaper, ButtonScissors],
                             ], one_time_keyboard=True))

def rock(update, context):
    context.bot.send_message(
        update.message.chat_id, 'You have choosen rock! 🪨', parse_mode=ParseMode.HTML)
    setMove(update, context, 1)

def paper(update, context):
    context.bot.send_message(
        update.message.chat_id, 'You have choosen paper! 📋', parse_mode=ParseMode.HTML)
    setMove(update, context, 2)

def scissors(update, context):
    context.bot.send_message(
        update.message.chat_id, 'You have choosen scissors! ✂️', parse_mode=ParseMode.HTML)
    setMove(update, context, 3)

def setMove(update, context, move):
    chatID = update.message.chat_id
    with open('games.json', 'r+') as data:
        fileData = json.load(data)
        for x in fileData['games']:
            # We set the choosen movement on the json file
            if x['player1ID'] == chatID:
                x['player1Movement'] = move
            if x['player2ID'] == chatID:
                x['player2Movement'] = move
    with open('games.json', 'w') as data:
        json.dump(fileData, data, indent=4)
    resolveRound(update, context)
# Restarts the movements of both players and adds (if necessary) a win to the winner
def newRound(update, context, winner):
    chatID = update.message.chat_id
    with open('games.json', 'r+') as data:
        fileData = json.load(data)
        for x in fileData['games']:
            # We set the choosen movement on the json file
            if x['player1ID'] == chatID or x['player2ID'] == chatID:
                x['player1Movement'] = 0
                x['player2Movement'] = 0
                if winner == 1:
                    x['player1Rounds'] += 1
                elif winner == 2:
                    x['player2Rounds'] += 1
    with open('games.json', 'w') as data:
        json.dump(fileData, data, indent=4)

def resolveRound(update, context):
    with open('games.json', 'r+') as data:
        chatID = update.message.chat_id
        fileData = json.load(data)
        player1Movement = 0
        player2Movement = 0
        for x in fileData['games']:
            # We set the choosen movement on the json file
            if x['player1ID'] == chatID or x['player2ID'] == chatID:
                player1Movement = x['player1Movement']
                player1ID = x['player1ID']
                player2Movement = x['player2Movement']
                player2ID = x['player2ID']
                player1Rounds = x['player1Rounds']
                player2Rounds = x['player2Rounds']
        with open('games.json', 'w') as data:
            json.dump(fileData, data, indent=4)
        if player1Movement != 0 and player2Movement != 0:
            if player1Movement == player2Movement+1 or player1Movement == player2Movement-2:
                veredict = 1
                player1Rounds += 1
            elif player1Movement == player2Movement-1 or player1Movement == player2Movement+2:
                veredict = 2
                player2Rounds += 1
            else:
                veredict = 3
            resolveRoundMessage(update, context, veredict, player1ID, player2ID, player1Movement, player2Movement, player1Rounds, player2Rounds)
            newRound(update, context, veredict)
            if player1Rounds >= NUMBER_ROUNDS_WIN or player2Rounds >= NUMBER_ROUNDS_WIN:
                endGame(update, context, player1ID, player2ID)
                startMenu(update,context, player1ID)
                startMenu(update,context, player2ID)
            else:
                send_movements(player1ID, context)
                send_movements(player2ID, context)

def endGame(update,context,player1ID,player2ID):
    with open('users.json', 'r+') as data:
        fileData = json.load(data)
        for x in fileData['userDetails']:
            if x['userID'] == player1ID or x['userID'] == player2ID:
                # We set the value 'inGame' false for the 2 players
                print('uwu')
                x['inGame'] = False
    with open('users.json', 'w') as data:
        json.dump(fileData, data, indent=4)
    with open('games.json', 'r+') as data:
        fileData = json.load(data)
        for idx, x in enumerate(fileData['games']):
            if x['player1ID'] == player1ID or x['player1ID'] == player2ID:
                x['isActive'] = False
                endedGame = x
                fileData['endedGames'].append(endedGame)
                fileData['games'].pop(idx)
    with open('games.json', 'w') as data:
        json.dump(fileData, data, indent=4)

#Sends the resolution of the rount to both players
def resolveRoundMessage(update, context, veredict, player1ID, player2ID, player1Movement, player2Movement, player1Rounds, player2Rounds):
    if player1Movement == 1:
        resultPlayer2 = '🪨 VS '
        resultPlayer1 = ' VS 🪨'
    elif player1Movement == 2:
        resultPlayer2 = '📋 VS '
        resultPlayer1 = ' VS 📋'
    else:
        resultPlayer2 = '✂️ VS '
        resultPlayer1 = ' VS ✂️'

    if player2Movement == 1:
        resultPlayer2 += '🪨'
        resultPlayer1 = '🪨' + resultPlayer1
    elif player2Movement == 2:
        resultPlayer2 += '📋'
        resultPlayer1 = '📋' + resultPlayer1
    else:
        resultPlayer2 += '✂️'
        resultPlayer1 = '✂️' + resultPlayer1

    context.bot.send_message(player1ID, resultPlayer1, parse_mode=ParseMode.HTML)
    context.bot.send_message(player2ID, resultPlayer2,parse_mode=ParseMode.HTML)

    if veredict == 1:
        context.bot.send_message(player1ID, 'You have won this round!\nRounds: You ['+str(player1Rounds)+'|'+str(player2Rounds)+'] Opponent', parse_mode=ParseMode.HTML)
        context.bot.send_message(player2ID, 'You have lost this round!\nRounds: You ['+str(player2Rounds)+'|'+str(player1Rounds)+'] Opponent', parse_mode=ParseMode.HTML)
    elif veredict == 2:
        context.bot.send_message(player2ID, 'You have won this round!\nRounds: You ['+str(player2Rounds)+'|'+str(player1Rounds)+'] Opponent', parse_mode=ParseMode.HTML)
        context.bot.send_message(player1ID, 'You have lost this round...\nRounds: You ['+str(player1Rounds)+'|'+str(player2Rounds)+'] Opponent', parse_mode=ParseMode.HTML)
    else:
        context.bot.send_message(player1ID, "It's a draw!", parse_mode=ParseMode.HTML)
        context.bot.send_message(player2ID, "It's a draw!", parse_mode=ParseMode.HTML)

    if player1Rounds >= NUMBER_ROUNDS_WIN:
        context.bot.send_message(player1ID, 'You have won this game!', parse_mode=ParseMode.HTML)
        context.bot.send_message(player2ID, 'You have lost this game... :(', parse_mode=ParseMode.HTML)
    elif player2Rounds >= NUMBER_ROUNDS_WIN:
        context.bot.send_message(player2ID, 'You have won this game!', parse_mode=ParseMode.HTML)
        context.bot.send_message(player1ID, 'You have lost this game... :(', parse_mode=ParseMode.HTML)
    
    print(player1ID)
    print(player2ID)

def startMenu(update,context, userID):
        context.bot.sendMessage(userID,
        text='Welcome! What do you want to do?',
        reply_markup=ReplyKeyboardMarkup([
            [Button1, Button2], [Button3, Button4]
        ])
    )

def changeMessage(update, context):
    context.bot.send_message(update.message.chat_id, 'What message do you want?', parse_mode=ParseMode.HTML, reply_markup = ForceReply())
    print(update.message.message)

def main():
    TOKEN = '5740883903:AAH369a_yh2OyYg11aTcbnW4AcffOmUW9D0'
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Eventos que activarán nuestro bot.
    # /comandos
    dp.add_handler(CommandHandler('start',    start))
    dp.add_handler(CommandHandler('startFriendly',    startFriendly))
    #dp.add_handler(CommandHandler('changeMessage',    changeMessage))

    dp.add_handler(CommandHandler('rock',    rock))
    dp.add_handler(CommandHandler('paper',    paper))
    dp.add_handler(CommandHandler('scissors',    scissors))

    dp.add_error_handler(error_callback)
    # Comienza el bot
    updater.start_polling()
    # Lo deja a la escucha. Evita que se detenga.
    updater.idle()


if __name__ == '__main__':
    print(('[Nombre del bot] Start...'))
    main()
