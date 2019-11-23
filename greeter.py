import discord
import logging

logging.basicConfig(level=logging.INFO)
bot = discord.Client()

@bot.event
async def on_ready():
	print(bot.user.id)

@bot.event
async def on_member_join(member):
	message = """Greetings, traveler! Our faq is in the welcome channel, feel free to make youself at home, and don't take any wooden nickels"""
	channel = next(x for x in member.guild.channels if x.name == "general")
	await channel.send(message)
	
bot.run('NTM5OTUyNTY0NzgzOTM5NTg5.DzJ7-A.icH0HJW9KyHX8BwAKNcvTet8OrM')