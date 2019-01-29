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
	for server in bot.servers:
		for member in server.members:
			if(yield from is_without_role(member)):
				yield from give_new_role(member)

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
		if role.name.startswith("balance: "):
			return False
	return True

@asyncio.coroutine
def give_new_role(member):
	role = yield from bot.create_role(member.server, name="balance: 1000")
	yield from bot.add_roles(member, role)


@asyncio.coroutine
def get_balance(member):
	for role in member.roles:
		if role.name.startswith("balance: "):
			balance = role.name.split("balance: ")[1]
			return balance
	yield

@asyncio.coroutine
def add_balance(member, amount):
	for role in member.roles:
		if role.name.startswith("balance: "):
			balance = role.name.split("balance: ")[1]
			new_amount = str(sympify(balance) + sympify(amount))
			if isnan(sreal(new_amount)) or isinf(sreal(new_amount)) or isnan(simag(new_amount)) or isinf(simag(new_amount)):
				return False
			newname = "balance: " + new_amount
			yield from bot.edit_role(member.server, role, name=newname)
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

@bot.command(pass_context=True,description='Gives eSpencoin to another member')
@asyncio.coroutine
def give(ctx, member : discord.Member, amount : str):
	yield from giveToPlayer(ctx, member, amount)

@bot.command(pass_context=True,description='Gives eSpencoin to everyone in a role')
@asyncio.coroutine
def giveall(ctx, role : discord.Role, amount : str):
	for member in role.server.members:
		if role in member.roles:
			author = ctx.message.author
			if member.id != bot.user.id and member.id != author.id:
				yield from giveToPlayer(ctx, member, amount)

bot.run('NTMzNDAzOTI2MDQxNDYwNzM2.DxqjdQ.YjWbPCT8Y8hJ36jAO6Xrbyh_Vg8')