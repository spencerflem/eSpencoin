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


starting_amount = 1000
balance_prefix = "balance "


@bot.event
async def on_ready():
    logging.info("Starting Up")
    for guild in bot.guilds:
        await give_starting_role_to_all_new_members(guild)
        await delete_all_orphans(guild)
    logging.info("Startup Complete!")


async def give_starting_role_to_all_new_members(guild):
    logging.info(f"Assiging Roles To Server: {guild.name}")
    starting_role = await make_or_find_role(guild, starting_amount)
    for member in guild.members:
        if is_without_role(member):
            await give_starting_role(member, starting_role)


async def give_starting_role(member, starting_role):
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
    await give_starting_role(member, starting_role)


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
    await member.remove_roles(role)
    new_role = make_or_find_role(member, amount)
    await member.add_roles(new_role)
    await delete_if_orphan(role)


def is_valid_amount(amount):
    if (
        isnan(sreal(new_amount))
        or isinf(sreal(new_amount))
        or isnan(simag(new_amount))
        or isinf(simag(new_amount))
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


async def add_balance(member, amount):
    balance = get_balance(member)  # TODO: IF NONE RETURN FALSE
    new_amount = add_amounts(balance, amount)  # TODO: IF NONE RETURN FALSE
    set_balance(member, new_amount)
    logging.info(
        f"Added: {amount} to: {member.name} With a Final Balance of: {new_amount}"
    )
    return True


async def giveToPlayer(to_member, from_member, amount):
    amount = sympify(amount)  # WHY SIMPIFY HERE? UNNEEDED?
    balance = get_balance(author)
    try:
        if member.id != bot.user.id and (  # TODO: IS VALID GIVE TARGET
            sreal(amount) == 0  # TODO: IS VALID GIVE AMOUNT
            or (sreal(balance) >= sreal(amount) and sreal(amount) >= 0)
        ):
            add1ok = await add_balance(member, amount)  #
            add2ok = await add_balance(
                author, -amount
            )  # TODO: SUBTRACT BALANCE? IS STRNG HERE...
            if add1ok and add2ok:
                print("GIVE")
                await bot.add_reaction(message, "👌")
            else:
                print("NO GIVE")
                await bot.add_reaction(message, "🙅")
                await bot.add_reaction(message, "👎")
        else:
            print("NO GIVE")
            await bot.add_reaction(message, "🙅")
            await bot.add_reaction(message, "🚫")
    except:
        print(sys.exc_info())
        await bot.add_reaction(message, "🙅")
        await bot.add_reaction(message, "❓")
    yield


def react_to_give(message, ENUM):
    pass


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
    status = await giveToPlayer(member, ctx.message.author, amount)
    await react_to_give(message, status)


@bot.command(pass_context=True, description="Gives eSpencoin to everyone in a role")
async def giveall(ctx, role: discord.Role, amount: str):
    for member in role.server.members:
        if role in member.roles:
            author = ctx.message.author
            if member.id != bot.user.id and member.id != author.id:  # IS_VALID_TARGET
                await giveToPlayer(ctx.message, member, ctx.message.author, amount)


bot.run("NTMzNDAzOTI2MDQxNDYwNzM2.DxqjdQ.YjWbPCT8Y8hJ36jAO6Xrbyh_Vg8")

# TODO: REORG WHOLE FILE

