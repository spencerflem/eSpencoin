import discord
import asyncio
import pexpect
from pexpect import popen_spawn

bot = discord.Client()
child = pexpect.popen_spawn.PopenSpawn("dfrotz zork1.z5")

def clean_msg():
    msg = child.before.decode('cp1252')
    print(msg)
    if len(msg.split("\n")) > 2:
        return "\n".join(msg.split("\n")[2:])
    else:
        return msg

@bot.event
@asyncio.coroutine 
def on_ready():
    print(bot.user.id)
    child.expect('>')
    for server in bot.servers:
        for channel in server.channels:
            if channel.name == "zork":
                yield from bot.send_message(channel, clean_msg())

@bot.event
@asyncio.coroutine 
def on_message(message):
    author = message.author
    channel = message.channel
    content = message.content
    if channel.name == "zork" and author != bot.user and not content.startswith("-"):
        child.sendline(content)
        child.expect(['>','filename'])
        msg = clean_msg()
        if msg != "":
            yield from bot.send_message(channel, clean_msg())
        

bot.run('NTM5NjgwODM1ODA5MzEyODA0.Dz_84A.Gbww6A94qEUXGKeYDmGeA9cn2E4')