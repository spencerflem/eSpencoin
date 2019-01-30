import discord
import asyncio
import threading
from discord.ext import commands

bot = discord.Client()

@bot.event
@asyncio.coroutine 
def on_ready():
    print(bot.user.id)

def is_valid_role(role):
    default_color = role.server.default_role.colour
    return role.colour == default_color and not role.name.startswith("balance: ")

@asyncio.coroutine
def clean(message):
    yield from asyncio.sleep(60)
    print("BYEEEEEE")
    yield from bot.delete_message(message)

@bot.event
@asyncio.coroutine 
def on_message(message):
    channel = message.channel
    author = message.author
    content = message.content
    if channel.name == "role-request":
        asyncio.ensure_future(clean(message))
        if content.startswith("!request "):
            requested_role = content.split("!request ",1)[1].strip('"')
            found = False
            given = False
            for role in channel.server.roles:
                if role.name == requested_role:
                    found = True
                    if is_valid_role(role):
                        given = True
                        yield from bot.add_roles(author, role)
                        yield from bot.add_reaction(message, '👌')
            if not found and not requested_role.startswith("balance: "):
                role = yield from bot.create_role(author.server, name=requested_role, mentionable=True)
                yield from bot.add_roles(author, role)
                yield from bot.add_reaction(message, '👌')
            elif found and not given:
                yield from bot.add_reaction(message, '🚫')
            elif requested_role.startswith("balance: "):
                yield from bot.add_reaction(message, '🚫')
        if content.startswith("!remove "):
            requested_role = content.split("!remove ",1)[1].strip('"')
            found = False
            for role in channel.server.roles:
                if role.name == requested_role:
                    found = True
                    yield from bot.remove_roles(author, role)
                    yield from bot.add_reaction(message, '👌')
            if not found:
                yield from bot.add_reaction(message, '🚫')


bot.run('NTM5OTUyNjM1NzQzMDQzNTk0.DzKQvA.NDnMOS19CW-nhYpkZSBWbJ_PL08')