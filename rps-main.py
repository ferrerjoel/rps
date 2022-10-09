# -*- coding: utf-8 -*-

from datetime import datetime
import json
from cgitb import text
import random
from shutil import move
from turtle import up, update
from telegram import *
from telegram.ext import *

import logging
# Telegram TOKEN
TOKEN = '5773831066:AAE9jjSHfF78zEa_FFjSgpP3vG5gmeMfLfU'
# Number of rounds in order to win
NUMBER_ROUNDS_WIN = 3
# Files
USERS_PATH = 'users.json'
GAMES_PATH = 'games.json'
# Help menu
HELP_MENU = "/help - Brief description of each command\n/start - Starts the bot and updates user information (username, firstname...)\n/game - Starts a game with a random player\n/message - Changes personal message\n/rock - Chooses rock 🪨\n/paper - Chooses paper 📋\n/scissors - Chooses scissors ✂️\n/availability - Changes your preferences to be chosen for random games"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
# Buttons
Button1 = KeyboardButton(
    text='Start game 🪨📋✂️'
)
Button2 = KeyboardButton(
    text='Change message 🎫'
)
Button3 = KeyboardButton(
    text='Change availability 📅'
)
Button4 = KeyboardButton(
    text='Help 📖'
)

ButtonRock = KeyboardButton(
    text='🪨'
)
ButtonPaper = KeyboardButton(
    text='📋'
)
ButtonScissors = KeyboardButton(
    text='✂️'
)

# Start method
def start(update, context):
    ''' START '''

    context.bot.send_message(update.message.chat_id,
                             'Welcome to RPS Project!', parse_mode=ParseMode.HTML)

    write_user_data(update.message.from_user.id, update.message.from_user.username,
                  update.message.from_user.first_name, update.message.from_user.last_name)

    start_menu(context, (update.message.chat_id))

# Creates a user on the JSON file
def write_user_data(userID, userName, firstName, lastName):
    newUserID = {'userID': userID, 'userName': userName, 'firstName': firstName,
                 'lastName': lastName, 'message' : "Hey there! I'm using RPS Project",'dateCreation': str(datetime.now()), 'inGame': False, 'available' : True, 'messageChange' : False}
    try:
        with open(USERS_PATH, 'r+') as data:
            fileData = json.load(data)
            needsUpdate = False
            if not any(userDetails['userID'] == userID for userDetails in fileData['userDetails']):
                fileData['userDetails'].append(newUserID)
                data.seek(0)
                json.dump(fileData, data, indent=4)
            else:
                # We check if the user has changed data from his Telegram profile
                needsUpdate = False
                for i in fileData['userDetails']:
                    if i['userID'] == userID:
                        if i['userName'] != userName:
                            i['userName'] = userName
                            needsUpdate = True
                        if i['firstName'] != firstName:
                            i['firstName'] = firstName
                            needsUpdate = True
                        if i['lastName'] != lastName:
                            i['lastName'] = lastName
                            needsUpdate = True
        if needsUpdate:
            with open(USERS_PATH, 'w') as data:
                json.dump(fileData, data, indent=4)
    except OSError as e:
        print(f"Unable to open {USERS_PATH}: {e}")
        return 
# Returns the userID of a user that is not in a game and that is available
def get_random_free_user_object(context, currentUserID):
    try:
        with open(USERS_PATH, 'r+') as data:
            fileData = json.load(data)
            userDetails = fileData['userDetails']
            userDetails = [x for x in userDetails if x['inGame'] == False and x['available'] == True and x['userID'] != currentUserID]
            if len(userDetails) >= 1 :
                opponentID = currentUserID
                while len(userDetails) >= 1:
                    print(currentUserID)
                    opponentID = random.choice(userDetails)['userID']
                    # Sending this message allows us to check if the choosen opponent has blocked the bot or not. The api does not provide a more elegant way of fixing this
                    try:
                        if opponentID != currentUserID:
                            # Message to see if it's blocked
                            context.bot.send_message(opponentID,
                                'You are being challenged!', parse_mode=ParseMode.HTML)
                            return opponentID
                    except:
                        for idx, x in enumerate(userDetails):
                            if x['userID'] == opponentID:
                                userDetails.pop(idx)
                        opponentID = currentUserID
            return None
    except OSError as e:
        print(f"Unable to open {USERS_PATH}: {e}")
        return 
# Checks if a user is in game
def user_is_in_game(userID):
    try:
        with open(USERS_PATH, 'r+') as data:
            fileData = json.load(data)
            userDetails = fileData['userDetails']
            for x in userDetails:
                # We set the choosen movement on the json file
                if x['userID'] == userID:
                    return x['inGame']
            return False
    except OSError as e:
        print(f"Unable to open {USERS_PATH}: {e}")
        return 
# Starts a game on the JSON file
def start_friendly(update, context):
    userID = update.message.from_user.id
    try:
        with open(GAMES_PATH, 'r+') as data:
            fileData = json.load(data)
            opponentID = get_random_free_user_object(context, userID)
            if not user_is_in_game(userID):
                if opponentID != None:
                    #if not any(userDetails['userID'] == opponentID for userDetails in fileData['games']):
                    print('Searching an opponent...')
                    # Player turn: 1 = Player 1 / 2 = Player 2 / 3 = Game ended
                    # Winner: 0 = game active / 1 = P1 / 2 = P2
                    newGame = {'player1ID': userID, 'player2ID': opponentID, 'gameStarted': str(datetime.now(
                    )), 'player1Movement': 0, 'player2Movement': 0, 'player1Rounds': 0, 'player2Rounds': 0, 'isActive' : True}
                    # We create a game on the database
                    fileData['games'].append(newGame)
                    data.seek(0)
                    json.dump(fileData, data, indent=4)
                    try:
                        with open(USERS_PATH, 'r+') as data:
                            fileData = json.load(data)
                            for x in fileData['userDetails']:
                                if x['userID'] == userID or x['userID'] == opponentID:
                                    # We set the value 'inGame' true for the 2 players
                                    x['inGame'] = True
                        with open(USERS_PATH, 'w') as data:
                            json.dump(fileData, data, indent=4)
                    except OSError as e:
                        print(f"Unable to open {USERS_PATH}: {e}")
                        return 
                    print(opponentID)
                    start_game(userID, opponentID, context)
                else:
                    print('No available players right now')
                    context.bot.send_message(update.message.chat_id, "There aren't any available players right now :(", parse_mode=ParseMode.HTML)
            else:
                context.bot.send_message(update.message.chat_id, "You are already in a game!", parse_mode=ParseMode.HTML)
    except OSError as e:
        print(f"Unable to open {GAMES_PATH}: {e}")
        return 
# Starts a game and sends the messages to users
def start_game(userID, opponentID, context):
    try:
        with open(USERS_PATH, 'r+') as data:
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
    except OSError as e:
        print(f"Unable to open {USERS_PATH}: {e}")
        return 

# Asks for the user input on movements
def send_movements(userID, context):
    context.bot.send_message(userID,
                             text='What move do you want to do?',
                             reply_markup=ReplyKeyboardMarkup([
                                 [ButtonRock, ButtonPaper, ButtonScissors],
                             ], one_time_keyboard=True))
# Puts the rock value on the JSON file
def rock(update, context):
    # We check if the user has already choosen
    if not check_player_turn(update, context):
        context.bot.send_message(
            update.message.chat_id, 'You have choosen rock! 🪨', parse_mode=ParseMode.HTML)
        # Sets the move on the JSON file
        set_move(update, context, 1)
    else: 
        context.bot.send_message(
            update.message.chat_id, 'You have already made your move!', parse_mode=ParseMode.HTML)
# Puts the paper value on the JSON file
def paper(update, context):
    if not check_player_turn(update, context):
        context.bot.send_message(
            update.message.chat_id, 'You have choosen paper! 📋', parse_mode=ParseMode.HTML)
        set_move(update, context, 2)
    else: 
        context.bot.send_message(
            update.message.chat_id, 'You have already made your move!', parse_mode=ParseMode.HTML)
# Puts the scissors value on the JSON file
def scissors(update, context):
    if not check_player_turn(update, context):
        context.bot.send_message(
            update.message.chat_id, 'You have choosen scissors! ✂️', parse_mode=ParseMode.HTML)
        set_move(update, context, 3)
    else: 
        context.bot.send_message(
            update.message.chat_id, 'You have already made your move!', parse_mode=ParseMode.HTML)
# returns True if the player has already choosen
def check_player_turn (update, context):
    chatID = update.message.chat_id
    try:
        with open(GAMES_PATH, 'r+') as data:
            fileData = json.load(data)
            for x in fileData['games']:
                # We set the choosen movement on the json file
                if x['player1ID'] == chatID:
                    return x['player1Movement'] != 0
                if x['player2ID'] == chatID:
                    return x['player2Movement'] != 0
            return False
    except OSError as e:
        print(f"Unable to open {GAMES_PATH}: {e}")
        return 
#Recives the user movement and sets the move on the JSON file
def set_move(update, context, move):
    chatID = update.message.chat_id
    try:
        with open(GAMES_PATH, 'r+') as data:
            fileData = json.load(data)
            for x in fileData['games']:
                # We set the choosen movement on the json file
                if x['player1ID'] == chatID:
                    x['player1Movement'] = move
                if x['player2ID'] == chatID:
                    x['player2Movement'] = move
        with open(GAMES_PATH, 'w') as data:
            json.dump(fileData, data, indent=4)
        resolve_round(update, context)
    except OSError as e:
        print(f"Unable to open {GAMES_PATH}: {e}")
        return 
# Restarts the movements of both players and adds (if necessary) a win to the winner
def new_round(update, context, winner):
    chatID = update.message.chat_id
    try:
        with open(GAMES_PATH, 'r+') as data:
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
        with open(GAMES_PATH, 'w') as data:
            json.dump(fileData, data, indent=4)
    except OSError as e:
        print(f"Unable to open {GAMES_PATH}: {e}")
        return 
# Takes the data of the game, if both players have made movements it chooses the winner
def resolve_round(update, context):
    try:
        with open(GAMES_PATH, 'r+') as data:
            chatID = update.message.chat_id
            fileData = json.load(data)
            player1Movement = 0
            player2Movement = 0
            for x in fileData['games']:
                # We take the data we need
                if x['player1ID'] == chatID or x['player2ID'] == chatID:
                    player1Movement = x['player1Movement']
                    player1ID = x['player1ID']
                    player2Movement = x['player2Movement']
                    player2ID = x['player2ID']
                    player1Rounds = x['player1Rounds']
                    player2Rounds = x['player2Rounds']
            with open(GAMES_PATH, 'w') as data:
                json.dump(fileData, data, indent=4)
    except OSError as e:
        print(f"Unable to open {USERS_PATH}: {e}")
        return 
        # Resolves the round: 1 = P1 Winner / 2 = P2 Winner / 3 = Draw
    if player1Movement != 0 and player2Movement != 0:
        if player1Movement == player2Movement+1 or player1Movement == player2Movement-2:
            veredict = 1
            player1Rounds += 1
        elif player1Movement == player2Movement-1 or player1Movement == player2Movement+2:
            veredict = 2
            player2Rounds += 1
        else:
            veredict = 3
        # We inform the players
        resolve_round_message(update, context, veredict, player1ID, player2ID, player1Movement, player2Movement, player1Rounds, player2Rounds)
        new_round(update, context, veredict)
        # We check if someone has already won
        if player1Rounds >= NUMBER_ROUNDS_WIN or player2Rounds >= NUMBER_ROUNDS_WIN:
            end_game(update, context, player1ID, player2ID)
            start_menu(context, player1ID)
            start_menu(context, player2ID)
        else:
            send_movements(player1ID, context)
            send_movements(player2ID, context)
# Ends the game on the JSON file. Moves the data of the game to the 'endedGames' object
def end_game(update,context,player1ID,player2ID):
    try:
        with open(USERS_PATH, 'r+') as data:
            fileData = json.load(data)
            for x in fileData['userDetails']:
                if x['userID'] == player1ID or x['userID'] == player2ID:
                    # We set the value 'inGame' false for the 2 players
                    x['inGame'] = False
        with open(USERS_PATH, 'w') as data:
            json.dump(fileData, data, indent=4)
    except OSError as e:
        print(f"Unable to open {USERS_PATH}: {e}")
        return
    try:
        with open(GAMES_PATH, 'r+') as data:
            fileData = json.load(data)
            for idx, x in enumerate(fileData['games']):
                if x['player1ID'] == player1ID or x['player1ID'] == player2ID:
                    x['isActive'] = False
                    endedGame = x
                    fileData['endedGames'].append(endedGame)
                    fileData['games'].pop(idx)
        with open(GAMES_PATH, 'w') as data:
            json.dump(fileData, data, indent=4)
    except OSError as e:
        print(f"Unable to open {USERS_PATH}: {e}")
        return 

#Sends the resolution of the rount to both players
def resolve_round_message(update, context, veredict, player1ID, player2ID, player1Movement, player2Movement, player1Rounds, player2Rounds):
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
# Shows the start menu
def start_menu(context, userID):
        context.bot.sendMessage(userID,
        text='What do you want to do?',
        reply_markup=ReplyKeyboardMarkup([
            [Button1, Button2], [Button3, Button4]
        ])
    )
# Changes the value of the user that allows to change the ussername
def change_message(update, context):
    context.bot.send_message(update.message.chat_id, 'What message do you want?', parse_mode=ParseMode.HTML, reply_markup = ForceReply())
    try:
        with open(USERS_PATH, 'r+') as data:
            fileData = json.load(data)
            for x in fileData['userDetails']:
                if x['userID'] == update.message.chat_id:
                    # We set the value 'inGame' false for the 2 players
                    x['messageChange'] = True
        with open(USERS_PATH, 'w') as data:
            json.dump(fileData, data, indent=4)
    except OSError as e:
        print(f"Unable to open {USERS_PATH}: {e}")
        return
# Changes the current user message
# We can't use a variable to know if the user wants to change the message, since a variable value is shared with all online users and it can generate problems
def update_message(update, context):
    try:
        with open(USERS_PATH, 'r+') as data:
            fileData = json.load(data)
        for x in fileData['userDetails']:
            if x['userID'] == update.message.chat_id:
                if x['messageChange']:
                    message = update.message.text
                    if len(message) < 50:
                # We set the value 'message' false so we know we have changed the message
                        x['message'] = message
                        x['messageChange'] = False
                        with open(USERS_PATH, 'w') as data:
                            json.dump(fileData, data, indent=4)
                        context.bot.send_message(update.message.chat_id, 'Message updated succesfully to: "'+ message + '"', parse_mode=ParseMode.HTML, reply_markup = ForceReply())
                    else:
                        context.bot.send_message(update.message.chat_id, "The message can't have more than 50 characters!", parse_mode=ParseMode.HTML, reply_markup = ForceReply())
    except OSError as e:
        print(f"Unable to open {USERS_PATH}: {e}")
        return 
    #If the user gets lost and doesn't know what to do a text message will always prompt the start menu
    start_menu(context, update.message.chat_id)
#Changes the availability value on the user object, this disables the posibility of beig choosen on a random game by another user
def change_availability(update, context):
    try:
        with open(USERS_PATH, 'r+') as data:
            fileData = json.load(data)
        for x in fileData['userDetails']:
            if x['userID'] == update.message.chat_id:
                if x['available']:
                    x['available'] = False
                    context.bot.send_message(update.message.chat_id,"From now on people can't start random games with you...", parse_mode=ParseMode.HTML)
                else:
                    x['available'] = True
                    context.bot.send_message(update.message.chat_id,"From now on people can start random games with you :)", parse_mode=ParseMode.HTML)
        with open(USERS_PATH, 'w') as data:
            json.dump(fileData, data, indent=4)
    except OSError as e:
        print(f"Unable to open {USERS_PATH}: {e}")
        return 
# Displays a user menu
def help(update, context):
    context.bot.send_message(update.message.chat_id, HELP_MENU, parse_mode=ParseMode.HTML)
# Main method
def main():
    global setMessage
    setMessage = False

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Eventos que activarán nuestro bot.
    # /comandos
    dp.add_handler(CommandHandler('start',    start))
    dp.add_handler(CommandHandler('game',    start_friendly))
    dp.add_handler(CommandHandler('message',    change_message))
    
    dp.add_handler(CommandHandler('rock',    rock))
    dp.add_handler(CommandHandler('paper',    paper))
    dp.add_handler(CommandHandler('scissors',    scissors))
    dp.add_handler(CommandHandler('help',    help))
    dp.add_handler(CommandHandler('availability',    change_availability))
    dp.add_handler(MessageHandler(Filters.text, command_translator))

    dp.add_error_handler(error_callback)
    # Comienza el bot
    updater.start_polling()
    # Lo deja a la escucha. Evita que se detenga.
    updater.idle()
# Reads every text that the user sends and if one matches a command it executes
# This way we can use buttons that doesn't has a "/command"
def command_translator(update,context):
    input = update.message.text
    if input == '🪨':
        rock(update, context)
    elif input == '📋':
        paper(update, context)
    elif input == '✂️':
        scissors(update, context)
    elif input == 'Start game 🪨📋✂️':
        start_friendly(update, context)
    elif input == 'Start':
        start(update, context)
    elif input == 'Change availability 📅':
        change_availability(update, context)
    elif input == 'Change message 🎫':
        change_message(update, context)
    elif input == 'Help 📖':
        help(update, context)
    else:
        update_message(update, context)

if __name__ == '__main__':
    print(('RPS Project starting...'))
    main()
