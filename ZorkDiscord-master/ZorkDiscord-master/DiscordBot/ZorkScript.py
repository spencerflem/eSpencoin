#!/usr/bin/python

import discord
import asyncio
import os
import datetime
from subprocess import Popen, PIPE

client = discord.Client()

def get_location():

	p = Popen(['./dungeon'], stdout=PIPE, stdin=PIPE)
	gameText = p.communicate(game_file.read())

	start = 0
	end = 0
	for i in range(len(gameText[0])-1, -1, -1):
		if chr(gameText[0][i]) == '>':
			if end == 0:
				end = i-1
			else:
				start = i+1
				break

	return gameText[0][start : end].decode("utf-8")

def remove_data(game_name, author_name):
	ret = True

	with open('__game_data__', 'r') as data_file:
		data_lines = data_file.readlines()
	
	with open('__game_data__', 'w') as data_file:
		for line in data_lines:
			if game_name not in line:
				data_file.write(line)
			elif author_name not in line:
				data_file.write(line)
				ret = False

	return ret

def add_data(game_name, author_name):
	with open('__game_data__', 'a') as data_file:
		now = datetime.datetime.now()
		data_file.write("**%s** -----  %s/%s/%s ----- %s:%s:%s ----- created by %s\n" % (game_name, now.month, now.day, now.year, now.hour, now.minute, now.second, author_name))

def reset():
	with open('__game_data__', 'w+') as data_file:
		data_lines = data_file.readlines()

	for line in data_lines:
		start = line.index('**') + len('**')
		end = line.rindex('**')
		os.remove(line[start:end])



@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_message(message):

	global game_file
	global data_file
	print('out')
	print(message.content.startswith('~Z '))
	print(message.author != client.user)
	print(message.channel.name == 'zork')
	if message.content.startswith('~Z ') and message.author != client.user and message.channel.name == 'zork':
		print('in')
		rest_of_content = message.content[3:]
		if rest_of_content.startswith('startGame'):
			file_name = rest_of_content[10:]
			file_name.strip()
			if not file_name:
				await client.send_message(message.channel, "You must give a name for the game you wish to start.")
				await client.send_message(message.channel, "The command must be in the form: `~Z startGame <game_name>`.")
			else:
				if game_file is 0: # we do not have an active game
					exists = os.path.isfile(file_name)
					if exists: # if the file already exists
						await client.send_message(message.channel, "The game **%s** already exists." % file_name)
						await client.send_message(message.channel, "If you would like to load this game try `~Z loadGame %s`." % file_name)
						await client.send_message(message.channel, "If you would like to delete this game try `~Z deleteGame %s`." % file_name)
					else: # if it doesnt exist, we need to create it
						game_file = open(file_name, 'w+b')
						add_data(file_name, str(message.author))
						await client.send_message(message.channel, "**%s** started." % file_name)
						await client.send_message(message.channel, "%s" % get_location())
				else: # we have an active game
					await client.send_message(message.channel, "You are currently in game **%s**." % game_file.name)
					await client.send_message(message.channel, "If you would like to start a new game you must end your current game using the command `~Z endGame`.")

		elif rest_of_content.startswith('endGame'):
			if game_file is 0: # we do not have an active game
				await client.send_message(message.channel, "You are not currently in a game.")
			else: # we have an active game
				await client.send_message(message.channel, "The game **%s** has ended." % game_file.name)
				game_file = 0

		elif rest_of_content.startswith('loadGame'):
			file_name = rest_of_content[9:]
			file_name.strip()
			if not file_name:
				await client.send_message(message.channel, "You must give a name for the game you wish to load.")
				await client.send_message(message.channel, "The command must be in the form: `~Z loadGame <game_name>`.")
			else:
				if game_file is 0: # we do not have an active game
					exists = os.path.isfile(file_name)
					if exists: # if the file already exists
						game_file = open(file_name, 'r+b')
						await client.send_message(message.channel, "The game **%s** has been successfully loaded." % file_name)
						await client.send_message(message.channel, "%s" % get_location())
					else: # the file does not exists
						await client.send_message(message.channel, "The game **%s** does not exist." % file_name)
						await client.send_message(message.channel, "If you would like to create a new game, use the command `~Z startGame %s`." % file_name)
						await client.send_message(message.channel, "For a list of all active games, use the command `~Z gameStats`.")
				else: # we have an active game
					await client.send_message(message.channel, "You are currently in game **%s**." % game_file.name)
					await client.send_message(message.channel, "If you would like to load a game you must end your current game using the command `~Z endGame`.")

		elif rest_of_content.startswith('deleteGame'):
			file_name = rest_of_content[11:]
			file_name.strip()
			if not file_name:
				await client.send_message(message.channel, "You must give a name for the game you wish to delete.")
				await client.send_message(message.channel, "The command must be in the form: `~Z deleteGame <game_name>`.")
			else:
				if game_file is not 0 and file_name == game_file.name: # if you try to delete a game currently in progress
					await client.send_message(message.channel, "The game **%s** is currently in progress." % file_name)
					await client.send_message(message.channel, "If you would like to delete the game, you must first end it by using the command `~Z endGame`.")
				else:
					exists = os.path.isfile(file_name)
					if exists: # if the file exists
						os.remove(file_name)
						if(remove_data(file_name, str(message.author))):
							await client.send_message(message.channel, "The game **%s** has been removed successfully." % file_name)
						else:
							await client.send_message(message.channel, "You must be the owner to delete that game.")
					else: # the file does not exist
						await client.send_message(message.channel, "The game **%s** does not exist." % file_name)

		elif rest_of_content.startswith('gameStats'):
			with open('__game_data__', 'r') as data_file:
				data_lines = data_file.read()
				if not data_lines:
					await client.send_message(message.channel, "There are no active games.")
				else:
					await client.send_message(message.channel, data_lines)

		elif rest_of_content.startswith('resetStats'):
			if str(message.author) != 'Matt#1077':
				await client.send_message(message.channel, "You do not have permission to use this command.")
			else:
				reset()
				await client.send_message(message.channel, "Reset.")

		elif rest_of_content.startswith('help'):
			help_text = """ 
```The following commands are used for the Zork game:
	~Z startGame <game_name>  : starts a new game.
	~Z loadGame <game_name>	  : loads a previous game.
	~Z deleteGame <game_name> : deletes a previous game.
	~Z endGame				  : ends the current game.
	~Z gameStats			  : lists all active games.
	~Z <input>				  : input Zork commands.
	~Z resetStats			  : removes all active games.
	~Z help					  : gets a list of all commands.```"""
			await client.send_message(message.channel, help_text)

		else:
			if game_file is 0:
				await client.send_message(message.channel, "You are not currently in a game.")
				await client.send_message(message.channel, "If you would like to start a new game, us the command `~Z startGame <game_name>`.")
			else:
				game_file.write((rest_of_content + '\n').encode("utf-8"))
				game_file.seek(0)
				await client.send_message(message.channel, "%s" % get_location())
		


game_file = 0
client.run('NTM5NjgwODM1ODA5MzEyODA0.DzF4eQ.VgUlav3yFG_NDX7mXqmjwU9Lp1c')
