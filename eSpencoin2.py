import discord
import asyncio
from discord.ext import commands
from sympy import sympify, evalf
from math import isnan, isinf
from itertools import groupby
import sys

bot = discord.Client()
bot = commands.Bot(command_prefix='!', description="The Central eSpencoin Exchange")

def scom(expr):
	return complex(sympify(expr).evalf())

def sreal(expr):
	return scom(expr).real

def simag(expr):
	return scom(expr).imag

@bot.event
@asyncio.coroutine 
def on_ready():
	for server in bot.servers:
		for member in server.members:
			if is_without_role(member):
				yield from give_new_role(member)
		for role in server.roles:
			yield from delete_if_orphan(role)

@bot.event
@asyncio.coroutine 
def on_error(event, *args):
	print("ERROEEE!")
	print(event)
	for arg in args:
		print(arg)
	print(sys.exc_info())
	yield
	
@bot.event
@asyncio.coroutine 
def on_member_join(member):
	yield from give_new_role(member)

def is_without_role(member):
	for role in member.roles:
		if role.name.startswith("balance: "):
			return False
	return True

@asyncio.coroutine
def give_new_role(member):
	role = yield from bot.create_role(member.server, name="balance: 0")
	yield from bot.add_roles(member, role)
	yield from add_balance(member, 1000)

def get_balance(member):
	for role in member.roles:
		if role.name.startswith("balance: "):
			balance = role.name.split("balance: ")[1]
			return balance
	return

def get_real_balance(member):
	return sreal(get_balance(member))

@asyncio.coroutine
def make_or_find_role(member, newname):
	for role in member.server.roles:
		if role.name == newname:
			yield from bot.add_roles(member, role)
			return
	new_role = yield from bot.create_role(member.server, name=newname, position=1)
	yield from bot.add_roles(member, new_role)

@asyncio.coroutine
def delete_if_orphan(test_role):
	is_orphan = False
	for member in test_role.server.members:
		for role in member.roles:
			if role == test_role:
				return
	yield from bot.delete_role(test_role.server, test_role)

@asyncio.coroutine
def add_balance(member, amount):
	for role in member.roles:
		if role.name.startswith("balance: "):
			balance = role.name.split("balance: ")[1]
			new_amount = str(sympify(balance) + sympify(amount))
			if isnan(sreal(new_amount)) or isinf(sreal(new_amount)) or isnan(simag(new_amount)) or isinf(simag(new_amount)):
				return False
			newname = "balance: " + new_amount
			yield from bot.remove_roles(member, role)
			yield from make_or_find_role(member, newname)
			yield from delete_if_orphan(role)
			return True
	return False

def giveToPlayer(message, give_to, give_from, amount):
	member = give_to
	author = give_from
	amount = sympify(amount)
	balance = get_balance(author)
	channel = message.channel
	try:
		if(member.id != bot.user.id and (sreal(amount) == 0 or (sreal(balance) >= sreal(amount) and sreal(amount) >= 0))):
			add1ok = yield from add_balance(member, amount) 
			add2ok = yield from add_balance(author, -amount)
			if( add1ok and add2ok ):
				print("GIVE")
				yield from bot.add_reaction(message, '👌')
			else:
				print("NO GIVE")
				yield from bot.add_reaction(message, '🙅')
				yield from bot.add_reaction(message, '👎')
		else:
			print("NO GIVE")
			yield from bot.add_reaction(message, '🙅')
			yield from bot.add_reaction(message, '🚫')
	except:
		print(sys.exc_info())
		yield from bot.add_reaction(message, '🙅')
		yield from bot.add_reaction(message, '❓')
	yield

@bot.event
@asyncio.coroutine
def on_reaction_add(reaction, user):
	try:
		if reaction.emoji.name == 'copperspoin':
			yield from giveToPlayer(reaction.message, reaction.message.author, user, "1")
		elif reaction.emoji.name == 'silverspoin':
			yield from giveToPlayer(reaction.message, reaction.message.author, user, "10")
		elif reaction.emoji.name == 'goldspoin':
			yield from giveToPlayer(reaction.message, reaction.message.author, user, "100")
		elif reaction.emoji.name == 'platinumspoin':
			yield from giveToPlayer(reaction.message, reaction.message.author, user, "1000")
	except AttributeError:
		pass
	yield

@bot.command(pass_context=True,description='Gives eSpencoin to another member')
@asyncio.coroutine
def give(ctx, member : discord.Member, amount : str):
	yield from giveToPlayer(ctx.message, member, ctx.message.author, amount)

@bot.command(pass_context=True,description='Gives eSpencoin to everyone in a role')
@asyncio.coroutine
def giveall(ctx, role : discord.Role, amount : str):
	for member in role.server.members:
		if role in member.roles:
			author = ctx.message.author
			if member.id != bot.user.id and member.id != author.id:
				yield from giveToPlayer(ctx.message, member, ctx.message.author, amount)

bot.run('NTMzNDAzOTI2MDQxNDYwNzM2.DxqjdQ.YjWbPCT8Y8hJ36jAO6Xrbyh_Vg8')