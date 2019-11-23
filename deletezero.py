import discord
import asyncio
from discord.ext import commands
from sympy import sympify, evalf
from math import isnan, isinf
from itertools import groupby
import sys

bot = discord.Client()
bot = commands.Bot(command_prefix='!', description="The Central eSpencoin Exchange")

@bot.event
@asyncio.coroutine 
def on_ready():
	for server in bot.servers:
		for role in server.roles:
			if role.name == "balance: 0":
				yield from bot.delete_role(server, role)
	print("DELETED!!")
	yield from bot.close()

bot.run('NTMzNDAzOTI2MDQxNDYwNzM2.DxqjdQ.YjWbPCT8Y8hJ36jAO6Xrbyh_Vg8')