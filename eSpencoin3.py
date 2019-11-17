import discord
import logging
from discord.ext import commands


from sympy import sympify
from math import isnan, isinf
from itertools import groupby
import sys


logging.basicConfig(level=logging.INFO)
bot = discord.Client()
bot = commands.Bot(command_prefix="!", description="The Central eSpencoin Exchange")

@bot.event
async def on_ready():
    logging.info("Starting Up")
    for guild in bot.guilds:
        await assign_starting_role_to_all_new_members(guild)
        await delete_all_orphans(guild)
    logging.info("Startup Complete!")


async def assign_starting_role_to_all_new_members(guild):
    logging.info(f"Assiging Roles To Server: {guild.name}")
    starting_role = await make_or_find_role(guild, starting_amount)
    for member in guild.members:
        if is_without_role(member):
            await assign_starting_role(member, starting_role)


async def assign_starting_role(member, starting_role):
    await member.add_roles(starting_role)
    logging.info(f"Gave starting role to: {member.name}")


async def delete_all_orphans(guild):
    logging.info(f"Deleting Ophans for Server: {guild.name}")
    for role in guild.roles:
        await delete_if_orphan(role)


def rolename_for_amount(amount):
    return balance_prefix + amount


async def make_or_find_role(guild, amount):
    rolename = rolename_for_amount(amount)
    for role in guild.roles:
        if role.name == rolename:
            return role
    new_role = await guild.create_role(name=rolename)
    new_role.position = 0
    return new_role


async def delete_if_orphan(role):
    if len(role.members) == 0:
        role.delete()
        logging.info(f"Deleted Role: {role.name}")


@bot.event
async def on_member_join(member):
    logging.info(f"Giving Role To New Member: {member.name}")
    starting_role = await make_or_find_role(member.guild, starting_amount)
    await assign_starting_role(member, starting_role)


def is_balance_role(role):
    return role.name.startswith(balance_prefix)


def get_balance_role_amount(role):
    return role.name.split(balance_prefix)[1]


def get_balance(member):
    role = get_balance_role(member)
    if role != None:
        return get_balance_role_amount(role)
    else:
        return None


def is_without_role(member):
    return get_balance_role(member) == None


def get_balance_role(member):
    for role in member.roles:
        if is_balance_role(role):
            return role
    return None


async def set_balance(member, amount):
    role = get_balance_role(member)
    if role == None:
        return False
    await member.remove_roles(role)
    new_role = make_or_find_role(member.guild, amount)
    await member.add_roles(new_role)
    await delete_if_orphan(role)
    return True


def is_valid_amount(amount):
    if (
        isnan(sreal(amount))
        or isinf(sreal(amount))
        or isnan(simag(amount))
        or isinf(simag(amount))
    ):
        return False
    else:
        return True

def add_amounts(amount1, amount2):
    sum_amount = str(sympify(amount1) + sympify(amount2))
    if is_valid_amount(sum_amount):
        return sum_amount
    else:
        return None

def subtract_amounts(amount1, amount2):
    diff_amount = str(sympify(amount1) - sympify(amount2))
    if is_valid_amount(diff_amount):
        return diff_amount
    else:
        return None

def add_balance(member, amount):
    balance = get_balance(member)
    if balance == None:
        return None
    else:
        return add_amounts(balance, amount)

def subtract_balance(member, amount):
    balance = get_balance(member)
    if balance == None:
        return None
    else:
        return subtract_amounts(balance, amount)

def is_valid_target(to_member, from_member):
    if to_member.id == bot.user.id or to_member.id == from_member.id:
        return False
    else:
        return True

def is_valid_give_amount_for_member(from_member, amount):
    if sreal(amount) < 0:
        return False
    elif sreal(amount) == 0:
        return simag(amount) != 0
    else: # sreal(amount) > 0
        balance = get_balance(from_member)
        if balance == None:
            return False
        else:
            return sreal(balance) >= sreal(amount)


async def giveToPlayer(to_member, from_member, amount):

    if not is_valid_target(to_member, from_member):
        return "INVALID_TARGET" #TODO: ENUM
    
    if not is_valid_give_amount_for_member(from_member, amount):
        return "INVALID_GIVE_AMOUNT"

    #TODO: GETS BALANCE TWICE!!

    to_balance = await add_balance(to_member, amount)
    from_balance = await subtract_balance(from_member, amount)

    if to_balance == None or from_balance == None:
        return "INVALID_BALANCE"

    await set_balance(to_member, to_balance)
    await set_balance(to_member)

async def react_to_give(message, ENUM):
    pass

async def give_and_react(message, to_member, from_member, amount):
    status = await giveToPlayer(to_member, from_member, amount)
    await react_to_give(message, status):

def scom(expr):
    return complex(sympify(expr).evalf())


def sreal(expr):
    return scom(expr).real


def simag(expr):
    return scom(expr).imag


@bot.event
async def on_reaction_add(reaction, user):
    # TODO: MUCH NICER WAY?
    # TODO: SHOULD BE SPLIT? Allows it to be forgotten
    try:
        if reaction.emoji.name == "copperspoin":
            await giveToPlayer(reaction.message, reaction.message.author, user, "1")
        elif reaction.emoji.name == "silverspoin":
            await giveToPlayer(reaction.message, reaction.message.author, user, "10")
        elif reaction.emoji.name == "goldspoin":
            await giveToPlayer(reaction.message, reaction.message.author, user, "100")
        elif reaction.emoji.name == "platinumspoin":
            await giveToPlayer(reaction.message, reaction.message.author, user, "1000")
    except AttributeError:
        pass
    yield


@bot.command(pass_context=True, description="Gives eSpencoin to another member")
async def give(ctx, member: discord.Member, amount: str):
    await give_and_react(ctx.message, member, ctx.message.author, amount)


@bot.command(pass_context=True, description="Gives eSpencoin to everyone in a role")
async def giveall(ctx, role: discord.Role, amount: str):
    for member in role.server.members:
        if role in member.roles:
            author = ctx.message.author
            if member.id != bot.user.id and member.id != author.id:  # IS_VALID_TARGET
                await give_and_react(ctx.message, member, author, amount)


bot.run("NTMzNDAzOTI2MDQxNDYwNzM2.DxqjdQ.YjWbPCT8Y8hJ36jAO6Xrbyh_Vg8")

# TODO: REORG WHOLE FILE (classes?)
# TODO: CONSISTENT LOGGING