#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Basic example for a bot that uses inline keyboards.
# This program is dedicated to the public domain under the CC0 license.

import globales
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler ,MessageHandler,Filters

# Necesarias para football-data.org
import http.client
import json



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(bot, update):

    globales.zona=0
    
    keyboard = [[InlineKeyboardButton("Quiero ver las competiciones disponibles", callback_data='1')],
                [InlineKeyboardButton("Otra Opción 2", callback_data='2')],
                [InlineKeyboardButton("Otra Opción 3", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Hola! Soy LigaFutbolBot. ¿Como puedo ayudarte?',reply_markup=reply_markup)
    


def update_id_table(chat_id,competition_id,team_id):
    found=0
    for k in range(0,len(globales.id_chat)):
        if globales.id_chat[k]==chat_id:
            globales.id_comp[k]=competition_id
            globales.id_team[k]=team_id
            found=1
            break
    if found==0:
        globales.id_chat.append(chat_id)
        globales.id_comp.append(competition_id)
        globales.id_team.append(team_id)

def get_id_comp(chat_id):
    found=0
    ret=0
    for k in range(0,len(globales.id_chat)):
        if globales.id_chat[k]==chat_id:
            found=1
            ret=str(globales.competition_list[-globales.id_comp[k]]['id']) 
            break
    if found==0:
        ret=0
    return ret

def get_id_team(chat_id):
    found=0
    ret=0
    for k in range(0,len(globales.id_chat)):
        if globales.id_chat[k]==chat_id:
            found=1
            ret=globales.id_team[k]
            break
    if found==0:
        ret=0
    return ret




def button(bot, update):
    query = update.callback_query
    


    
    if globales.zona == 0:  # Zona 0 es el menú principal segun se empieza
        if str(query.data) == "1":
            update_id_table(query.message.chat_id,0,0)  # we save chat_id ,nothing else chosen yet
            globales.zona = 1
            bot.editMessageText(text= show_competitions_list(), chat_id=query.message.chat_id, message_id=query.message.message_id)
            ask_competition(bot, update)
    elif globales.zona == 1:  # Zona 1 es la selección de competición
        if int(query.data) >= 1 and int(query.data) <= globales.available_competitions:
            update_id_table(query.message.chat_id,int(query.data),0)  # we now know the selected competition
            globales.zona = 2
            bot.editMessageText(text=show_one_competition(int(query.data)), chat_id=query.message.chat_id, message_id=query.message.message_id)
            ask_one_competition(bot,update)
    elif globales.zona == 2 : # Inmediatamente después de que se le muestre información sobre una competición
        if query.data == "1":  # Quiere ver una lista de los equipos participantes
            globales.zona=3
            bot.editMessageText(text= show_team_list(update), chat_id=query.message.chat_id, message_id=query.message.message_id)
        if query.data == "2":  # Quiere ver una clasificación a día de hoy
            globales.zona=4
            bot.editMessageText(text= show_leaguetable(update), chat_id=query.message.chat_id, message_id=query.message.message_id)
        #if query.data == "3":  # Quiere ver una lista de proximos enfrentamientos
        #if query.data == "4":  # Quiere ver información de un equipo en particular
        if query.data == "5":  # Quiere seleccionar otra competición diferente
            update_id_table(query.message.chat_id,0,0)  # we save chat_id ,nothing else chosen yet
            globales.zona = 1
            bot.editMessageText(text= show_competitions_list(), chat_id=query.message.chat_id, message_id=query.message.message_id)
            ask_competition(bot, update)
            
            

        
        
        


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))

def echo(bot, update):
    update.message.reply_text(update.message.text)

# ------------------------------------------------------------------------------
#                            Datos de football-data.org
# ------------------------------------------------------------------------------
def get_competitions():
    try:
        connection = http.client.HTTPConnection('api.football-data.org')
        headers = { 'X-Auth-Token': '97aec86ffe4d4f2c82f17492a6bca093', 'X-Response-Control': 'minified' }
        connection.request('GET', '/v1/competitions', None, headers )
        response = json.loads(connection.getresponse().read().decode())
    except:
        print("There was a problem getting the competition information")
        response = ""
    return response





def show_competitions_list():
    globales.competition_list = get_competitions()
    globales.available_competitions = len(globales.competition_list)
    cad = ""
    cad += "Competiciones Disponibles: " +  str(globales.available_competitions) + chr(10) + chr(10)
    for x in range(1, globales.available_competitions):
        competition_row = str(x) + ".- " + str(globales.competition_list[-x]['caption'])  
        cad += competition_row + chr(10)
    return cad

def ask_competition(bot, update):
    
    if globales.available_competitions>8:
        keyboard_competitions1 = []
        keyboard_competitions2 = []
        for x in range(1, 8):
            keyboard_competitions1.append(InlineKeyboardButton(str(x), callback_data= str(x)))
        for x in range(9, globales.available_competitions):
            keyboard_competitions2.append(InlineKeyboardButton(str(x), callback_data= str(x)))
        keyboard = [keyboard_competitions1,keyboard_competitions2]
    else:
        keyboard_competitions1 = []
        for x in range(1, globales.available_competitions):
            keyboard_competitions.append(InlineKeyboardButton(str(x), callback_data= str(x)))
        keyboard = [keyboard_competitions1]

    reply_markup = InlineKeyboardMarkup(keyboard)
    chat_id=update.callback_query.message.chat_id
    bot.sendMessage(chat_id,text='Sobre que competición quieres ver información?', reply_markup=reply_markup)
    

    
def show_one_competition(competition_number):
    x=competition_number
    cad = ""
    cad += str(globales.competition_list[-x]['caption'] + chr(10) + chr(10))
    cad += "Equipos participantes: " + str(globales.competition_list[-competition_number]['numberOfTeams']) + chr(10)
    cad += "Número de partidos: " + str(globales.competition_list[-x]['numberOfGames'])+chr(10)
    cad += "Número de Jornadas: " + str(globales.competition_list[-x]['numberOfMatchdays']) + chr(10)
    cad += "Jornada en Curso: "+str(globales.competition_list[-x]['currentMatchday'])+chr(10)

    return cad


def ask_one_competition(bot,update):
    keyboard=[[InlineKeyboardButton("Quieres ver una lista de los equipos participantes?", callback_data='1')],
              [InlineKeyboardButton("Quieres ver la clasificación a día de hoy?", callback_data='2')],
              [InlineKeyboardButton("Quieres ver una lista con los próximos enfrentamientos?", callback_data='3')],
              [InlineKeyboardButton("Quieres ver información sobre el equipo?", callback_data='4')],
              [InlineKeyboardButton("Prefieres seleccionar otra competición?", callback_data='5')]]
    reply_markup=InlineKeyboardMarkup(keyboard)
    chat_id=update.callback_query.message.chat_id
    bot.sendMessage(chat_id,text='Que opción prefieres?', reply_markup=reply_markup)
    

def get_teams(update):
    try:
        connection = http.client.HTTPConnection('api.football-data.org')
        headers = { 'X-Auth-Token': '97aec86ffe4d4f2c82f17492a6bca093', 'X-Response-Control': 'minified' }
        connection.request('GET', '/v1/competitions/'+str(get_id_comp(update.callback_query.message.chat_id))+'/teams', None, headers )
        response = json.loads(connection.getresponse().read().decode())
    except:
        print("There was a problem getting the competition information")
        response = ""
    return response


def show_team_list(update):
    team_list = get_teams(update)
    print(team_list)
    available_teams = team_list['count']
    cad = ""
    cad += "Equipos participantes: " +  str(available_teams) + chr(10) + chr(10)
    for x in range(0, available_teams):
        team_row = str(x) + ".- " + str(team_list['teams'][-x]['name'])  
        cad += team_row + chr(10)
    return cad


def get_leaguetable(update):
    try:
        connection = http.client.HTTPConnection('api.football-data.org')
        headers = { 'X-Auth-Token': '97aec86ffe4d4f2c82f17492a6bca093', 'X-Response-Control': 'minified' }
        connection.request('GET', '/v1/competitions/'+str(get_id_comp(update.callback_query.message.chat_id))+'/leagueTable', None, headers )
        response = json.loads(connection.getresponse().read().decode())
    except:
        print("There was a problem getting the competition information")
        response = ""
    return response

def show_leaguetable(update):
    liga_id=get_id_comp(update.callback_query.message.chat_id)
    lista = get_leaguetable(update)
    print(lista)
    leagueCaption=lista['leagueCaption']
    matchday=lista['matchday']
    try:
        long = len(lista['standings'])
        header='standings'
    except:
        long = len(lista['standing'])
        header='standing'
    cad = ""
    cad += leagueCaption +chr(10)+chr(10)
    cad += "Clasificación Jornada: " + str(matchday) + chr(10)+chr(10)
    cad += "  " + " " + "Nombre del Equipo" + " " + "PJ" + " " + "PT" +" "+ "GL"+" "+ "GF" +" "+ "GC"+chr(10)
    for x in range(0, long):
        #if liga_id==0: header='standings'
        #else: 
        header='standing'
        nombre_equipo=str(lista[header][-x]['team'])
        long_nombre_equipo=len(nombre_equipo)
        num_espacios="."*(17-long_nombre_equipo)
        row = str(x) + " " + nombre_equipo+num_espacios + " " + str(lista[header][-x]['playedGames']) + " " + str(lista[header][-x]['points']) + " " + str(lista[header][-x]['goals']) + " " + str(lista[header][-x]['goalsAgainst']) + " " + str(lista[header][-x]['goalDifference'])
        cad += row + chr(10)
    return cad

    

def main():

    # Create the Updater and pass it your bot's token.
    updater = Updater("318936108:AAH-DN8_8EEvcE5n7X7KPMz-E7s7t8JABPE")
    
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    #updater.dispatcher.add_handler(CommandHandler('ask_competition', ask_competition))
    
    
    updater.dispatcher.add_error_handler(error)
    
    # Start the Bot
    updater.start_polling()
    
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()