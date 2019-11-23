import discord
import logging

logging.basicConfig(level=logging.INFO)
bot = discord.Client()

@bot.event
async def on_ready():
	print(bot.user.id)

@bot.event
async def on_message(message):
	if "uwu" in message.content.lower() and not message.author == bot.user :
	    await message.channel.send("UWU'S ARE GLOBALLY BANNED. PLEASE REPORT FOR MANDATORY TERMINATION. THANK YOU FOR YOUR COMPLIANCE.")
	
bot.run('NjQ3MTY2MTIxMDkwMjIwMDMy.Xdbuxg.F1MwNYg5Mape79EXvOX86T0RvrA')