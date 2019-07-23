import discord
import asyncio
from discord.ext import commands
from sympy import sympify, evalf
from math import isnan, isinf
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
	print(bot.user.id)
	for server in bot.servers:
		for member in server.members:
			if(yield from is_without_role(member)):
				yield from give_new_role(member)
		for role in server.roles:
			yield from delete_if_orphan(role)
	print("DONE")

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

@asyncio.coroutine 
def is_without_role(member):
	for role in member.roles:
		if role.name.startswith("toes: "):
			return False
	return True

@asyncio.coroutine
def give_new_role(member):
	role = yield from bot.create_role(member.server, name="toes: 0")
	yield from bot.add_roles(member, role)
	yield from add_balance(member, 10)

@asyncio.coroutine
def get_balance(member):
	for role in member.roles:
		if role.name.startswith("toes: "):
			balance = role.name.split("toes: ")[1]
			return balance
	yield

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
		if role.name.startswith("toes: "):
			balance = role.name.split("toes: ")[1]
			new_amount = str(sympify(balance) + sympify(amount))
			if isnan(sreal(new_amount)) or isinf(sreal(new_amount)) or isnan(simag(new_amount)) or isinf(simag(new_amount)):
				return False
			newname = "toes: " + new_amount
			yield from bot.remove_roles(member, role)
			yield from make_or_find_role(member, newname)
			yield from delete_if_orphan(role)
			return True
	return False

def giveToPlayer(ctx, member, amount):
	author = ctx.message.author
	amount = sympify(amount)
	balance = yield from get_balance(author)
	channel = ctx.message.channel
	try:
		if(member.id != bot.user.id and member.id != author.id and (sreal(amount) == 0 or (sreal(balance) >= sreal(amount) and sreal(amount) >= 0))):
			add1ok = yield from add_balance(member, amount) 
			add2ok = yield from add_balance(author, -amount)
			if( add1ok and add2ok ):
				print("GIVE")
				yield from bot.add_reaction(ctx.message, '👌')
			else:
				print("NO GIVE")
				yield from bot.add_reaction(ctx.message, '🙅')
				yield from bot.add_reaction(ctx.message, '👎')
		else:
			print("NO GIVE")
			yield from bot.add_reaction(ctx.message, '🙅')
			yield from bot.add_reaction(ctx.message, '🚫')
	except:
		print(sys.exc_info())
		yield from bot.add_reaction(ctx.message, '🙅')
		yield from bot.add_reaction(ctx.message, '❓')
	yield

@bot.command(pass_context=True,description='Gives toes to another member')
@asyncio.coroutine
def bequeath(ctx, member : discord.Member, amount : str):
	yield from giveToPlayer(ctx, member, amount)

@bot.command(pass_context=True,description='Gives toes to everyone in a role')
@asyncio.coroutine
def bequeathuniversally(ctx, role : discord.Role, amount : str):
	for member in role.server.members:
		if role in member.roles:
			author = ctx.message.author
			if member.id != bot.user.id and member.id != author.id:
				yield from giveToPlayer(ctx, member, amount)

bot.run('NTQyMjA5NzAwMDkxOTIwMzk3.DzqsCw.SPvbTdCvCnwo9wTj7eo3RXJzx9w')