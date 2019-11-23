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

emoji_amounts = {
    "copperspoin": 1,
    "silverspoin": 10,
    "goldspoin": 100,
    "platinumspoin": 1000,
}

economies = {}


def get_role_balance(role):
    return role.name.split(balance_prefix)[1]


def is_balance_role(role):
    return get_role_balance(role) != None


def start_economy(guild):
    economies[guild.id] = Economy(guild).start()


def update_member(member):
    economies[member.guild.id].update_member(member)


def create_if_balance(role):
    amount = get_role_balance(role)
    if amount != None:
        economies[role.guild.id].balance_roles[role.id] = amount


async def delete_if_balance(role):
    if is_balance_role:
        economy = economies[role.guild.id]
        del economy.balance_roles[role.id]
        for member in role.members:
            await economy.assign_starting_role(member)


def update_if_balance(role):
    amount = get_role_balance(role)
    if amount != None:
        economies[role.guild.id].update_balance_role(role, amount)


async def assign_starting_role(member):
    await economies[member.guild.id].assign_starting_role(member)


async def give_if_reaction(emoji, to_member, from_member):
    amount = emoji_amounts[emoji.name]
    if amount != None:
        economies[from_member.guild.id].give(to_member, from_member, amount)


def give_is_valid(to_member, from_member, amount):
    pass


async def give_if_valid(to_member, from_member, amount):
    if give_is_valid(to_member, from_member, amount):
        economies[from_member.guild.id].give(to_member, from_member, amount)


class Economy:

    balance_roles = {}
    starting_role = None
    member_balances = {}

    def __init__(self):
        pass

    async def start(self, guild):
        self.map_balance_roles(guild)
        self.map_members_balances(guild)
        self.assign_starting_roles_to_new_members()
        # DELETE ALL ORPHANS
        pass

    def update_balance_role(self, role, amount):
        self.balance_roles[role.id] = amount
        for member in role.members:
            self.member_balances[member.id] = amount
        # DEAL WITH STARTING ROLE

    def add_all_members(self, guild):
        starting_role = make_or_find_role()
        for member in guild.members:
            self.citizens[member.id] = Citizen(member, starting_role)


class Citizen:

    member

    def __init__(
        self, member,
    ):
        self._member = member
        self._balance_role = self._get_or_assign_balance_role(starting_role)

    def _get_or_assign_balance_role(self, starting_role):
        for role in member.roles:
            if is_balance_role(role):
                return role

        return


async def react(message, status):
    pass


@bot.event
async def on_ready():
    for guild in bot.guilds:
        await start_economy(guild)


@bot.event
async def on_member_join(member):
    await assign_starting_role(member)


@bot.event
async def on_member_update(before, after):
    update_member(after)


@bot.event
async def on_guild_role_create(role):
    create_if_balance(role)


@bot.event
async def on_guild_role_delete(role):
    await delete_if_balance(role)


@bot.event
async def on_guild_role_update(before, after):
    update_if_balance(after)


@bot.event
async def on_reaction_add(reaction, user):
    await give_if_reaction(reaction.emoji, reaction.message.author, user)


@bot.command(pass_context=True, description="Gives eSpencoin to another member")
async def give(ctx, member: discord.Member, amount: str):
    status = await give(member, ctx.message.author, amount)
    await react(ctx.message, status)


@bot.command(pass_context=True, description="Gives eSpencoin to everyone in a role")
async def giveall(ctx, role: discord.Role, amount: str):
    for member in role.members:
        author = ctx.message.author
        status = await give_if_valid(member, author, amount)
        await react(ctx.message, status)


bot.run("NTMzNDAzOTI2MDQxNDYwNzM2.DxqjdQ.YjWbPCT8Y8hJ36jAO6Xrbyh_Vg8")
