import discord # Imported from https://github.com/Rapptz/discord.py
import asyncio
from discord.ext import commands

# A dice bot for use with Discord
bot = discord.Client()
bot = commands.Bot(command_prefix='!', description="The Central eSpencoin Exchange")

# Determines if a message is owned by the bot
def is_me(m):
	return m.author == bot.user

# Determines if the value can be converted to an integer
# Parameters: s - input string
# Returns: boolean. True if can be converted, False if it throws an error.
def is_num(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

@bot.event
@asyncio.coroutine 
def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')
	for server in bot.servers:
		for member in server.members:
			if(yield from is_without_role(member)):
				yield from give_zero_role(member)

@bot.event
@asyncio.coroutine 
def on_member_join(member):
    yield from give_zero_role(member)

@asyncio.coroutine 
def is_without_role(member):
	for role in member.roles:
		if role.name.startswith("balance: "):
			return False
	return True

@asyncio.coroutine
def give_zero_role(member):
	role = yield from bot.create_role(member.server, name="balance: 0")
	yield from bot.add_roles(member, role)


@asyncio.coroutine
def get_balance(member):
	for role in member.roles:
		if role.name.startswith("balance: "):
			balance = int(role.name.split("balance: ")[1])
			return balance
	yield

#todo, test infinity and nan
@asyncio.coroutine
def add_balance(member, amount):
	for role in member.roles:
		if role.name.startswith("balance: "):
			balance = int(role.name.split("balance: ")[1])
			newname = "balance: " + str(balance + amount)
			yield from bot.edit_role(member.server, role, name=newname)
	yield


@bot.command(pass_context=True,description='Gives eSpencoin to another member')
@asyncio.coroutine
def give(ctx, member : discord.Member, amount : int):
	author = ctx.message.author
	balance = yield from get_balance(author)
	if(balance >= amount and amount > 0):
		yield from add_balance(member, amount)
		yield from add_balance(author, -amount)
	yield

@bot.command(pass_context=True,description='Mints new eSpencoin fresh off the press')
@asyncio.coroutine
def award(ctx, member : discord.Member, amount : int):
	channel = ctx.message.channel
	if(channel.id == "533444271005761566"):
		yield from add_balance(member, amount)
	yield
	
#Bot command to delete all messages the bot has made.		 
@bot.command(pass_context=True,description='Deletes all messages the bot has made')
@asyncio.coroutine
def purge(ctx):
	channel = ctx.message.channel
	deleted = yield from bot.purge_from(channel, limit=100, check=is_me)
	yield from bot.send_message(channel, 'Deleted {} message(s)'.format(len(deleted)))

# Follow this helpful guide on creating a bot and adding it to your server. 
# https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token
bot.run('NTMzNDAzOTI2MDQxNDYwNzM2.DxqjdQ.YjWbPCT8Y8hJ36jAO6Xrbyh_Vg8')
