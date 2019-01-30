import discord
import asyncio

bot = discord.Client()

@bot.event
@asyncio.coroutine 
def on_ready():
	print(bot.user.id)

@bot.event
@asyncio.coroutine 
def on_member_join(member):
	message = """Greetings, traveler! Our faq is in the welcome channel, feel free to make youself at home, and don't take any wooden nickels"""
	channel = next(x for x in member.server.channels if x.name == "general")
	yield from bot.send_message(channel, message)
	
bot.run('NTM5OTUyNTY0NzgzOTM5NTg5.DzJ7-A.icH0HJW9KyHX8BwAKNcvTet8OrM')